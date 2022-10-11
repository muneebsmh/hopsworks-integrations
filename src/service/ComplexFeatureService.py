import hsfs.constructor.query
import logging
import pandas as pd
from hsfs.feature import Feature
import json
import sys
import os

parent_dir = os.path.dirname(os.getcwd())
sys.path.insert(0,parent_dir)

from src.service import FeatureStoreService as fss
from src.utils import multi_melt as melt
logger = logging.getLogger('logger')


class ComplexFeatureService:
    def __init__(self, config):
        self.conf = config
        with open(self.conf, "r") as jsonfile:
            data = json.load(jsonfile)

    def build_view_team(self):
        try:
            logger.info('Getting feature groups details')
            features_game_base = ["uuid", "League", "Date", "Team1", "Team2", "Season", "G_Type", "T1_loc", "T2_loc",
                                  "T1_sea_g_played", "T1_sea_g_played_h", "T1_sea_g_played_a", "T2_sea_g_played",
                                  "T2_sea_g_played_h", "T2_sea_g_played_a", "T1_B2B", "T2_B2B"]
            features_box_score = ["T1_pts", "T2_pts", "T1_Result", "T2_Result", "Box_Type", "MP", "T1_FGM", "T1_FGA",
                                  "T1_FG_Pct", "T1_2PM", "T1_2PA", "T1_2P_Pct", "T1_3PM", "T1_3PA", "T1_3P_Pct",
                                  "T1_FTM", "T1_FTA", "T1_FT_Pct", "T1_OREB", "T1_DREB", "T1_REB", "T1_AST", "T1_TOV",
                                  "T1_STL", "T1_BLK", "T1_PF", "T2_FGM", "T2_FGA", "T2_FG_Pct", "T2_2PM", "T2_2PA",
                                  "T2_2P_Pct", "T2_3PM", "T2_3PA", "T2_3P_Pct", "T2_FTM", "T2_FTA", "T2_FT_Pct",
                                  "T2_OREB", "T2_DREB", "T2_REB", "T2_AST", "T2_TOV", "T2_STL", "T2_BLK", "T2_PF",
                                  "PD_Box", "PT_Box"]
            features_adv_stats = ["T1_Poss_Cnt", "T1_Poss_Sec", "T1_Poss_Sdp", "Box_Type", "T1_FGA_Poss_Prop",
                                  "T1_2PA_Poss_Prop", "T1_3PA_Poss_Prop", "T1_FTA_Poss_Prop", "T1_FTA_FGA_Rto",
                                  "T1_EFG_Pct", "T1_TS_Pct", "T1_OREB_REB_Pct", "T1_DREB_REB_Pct", "T1_TOV_Poss_Pct",
                                  "T1_PF_Poss_Pct", "T2_Poss_Cnt", "T2_Poss_Sec", "T2_Poss_Sdp", "T2_FGA_Poss_Prop",
                                  "T2_2PA_Poss_Prop", "T2_3PA_Poss_Prop", "T2_FTA_Poss_Prop", "T2_FTA_FGA_Rto",
                                  "T2_EFG_Pct", "T2_TS_Pct", "T2_OREB_REB_Pct", "T2_DREB_REB_Pct", "T2_TOV_Poss_Pct",
                                  "T2_PF_Poss_Pct", "PD_Poss", "PT_Poss"]
            fss_obj = fss.FeatureStoreService(self.conf)
            fg_game_base = fss_obj.get_group(
                "gp_game_base",
                2
            )

            fg_box_score = fss_obj.get_group(
                "gp_box_score",
                1
            )

            fg_adv_stats = fss_obj.get_group(
                "gp_adv_stats",
                1
            )

            df = fg_box_score.select(features_box_score).filter(Feature('uuid') == 6568) \
                .join(fg_adv_stats.select(features_adv_stats).filter(Feature('uuid') == 6568), \
                      on=['uuid', 'box_type'], join_type='inner') \
                .join(fg_game_base.select(features_game_base).filter(Feature('uuid') == 6568), \
                      on=['uuid'], join_type='inner') \
                .read()

            df['t1_pd_box'] = df['t2_pts'] - df['t1_pts']
            df['t2_pd_box'] = df['t1_pts'] - df['t2_pts']

            df['t1_pd_poss'] = (df['t2_pts'] - df['t1_pts']) / (df[['t1_poss_cnt', 't2_poss_cnt']].mean(axis=1))
            df['t2_pd_poss'] = (df['t1_pts'] - df['t2_pts']) / (df[['t1_poss_cnt', 't2_poss_cnt']].mean(axis=1))

            id_vars = ['uuid', 'date', 'season', 'box_type', 'g_type', 'mp', 'pt_box', 'pt_poss']

            value_vars = [['Team1', 'Team2'], ['T1_Loc', 'T2_Loc'], ['T1_sea_g_played', 'T2_sea_g_played'],
                          ['T1_B2B', 'T2_B2B'], ['t1_pd_box', 't2_pd_box'], ['t1_pd_poss', 't2_pd_poss'],
                          ['T1_PTS', 'T2_PTS'], ['T1_FGM', 'T2_FGM'], ['T1_FGA', 'T2_FGA'],
                          ['T1_FG_Pct', 'T2_FG_Pct'], ['T1_2PM', 'T2_2PM'], ['T1_2PA', 'T2_2PA'],
                          ['T1_2P_Pct', 'T2_2P_Pct'],
                          ['T1_3PM', 'T2_3PM'], ['T1_3PA', 'T2_3PA'], ['T1_3P_Pct', 'T2_3P_Pct'], ['T1_FTM', 'T2_FTM'],
                          ['T1_FTA', 'T2_FTA'], ['T1_FT_Pct', 'T2_FT_Pct'], ['T1_OREB', 'T2_OREB'],
                          ['T1_DREB', 'T2_DREB'],
                          ['T1_REB', 'T2_REB'], ['T1_AST', 'T2_AST'], ['T1_TOV', 'T2_TOV'], ['T1_STL', 'T2_STL'],
                          ['T1_BLK', 'T2_BLK'],
                          ['T1_PF', 'T2_PF'], ['T2_PTS', 'T1_PTS'], ['T2_FGM', 'T1_FGM'], ['T2_FGA', 'T1_FGA'],
                          ['T2_FG_Pct', 'T1_FG_Pct'], ['T2_2PM', 'T1_2PM'], ['T2_2PA', 'T1_2PA'],
                          ['T2_2P_Pct', 'T1_2P_Pct'],
                          ['T2_3PM', 'T1_3PM'], ['T2_3PA', 'T1_3PA'], ['T2_3P_Pct', 'T1_3P_Pct'], ['T2_FTM', 'T1_FTM'],
                          ['T2_FTA', 'T1_FTA'], ['T2_FT_Pct', 'T1_FT_Pct'], ['T2_OREB', 'T1_OREB'],
                          ['T2_DREB', 'T1_DREB'],
                          ['T2_REB', 'T1_REB'], ['T2_AST', 'T1_AST'], ['T2_TOV', 'T1_TOV'], ['T2_STL', 'T1_STL'],
                          ['T2_BLK', 'T1_BLK'],
                          ['T2_PF', 'T1_PF'], ['T1_Poss_Cnt', 'T2_Poss_Cnt'], ['T1_Poss_Sec', 'T2_Poss_Sec'],
                          ['T1_Poss_Sdp', 'T2_Poss_Sdp'], ['T1_FGA_Poss_Prop', 'T2_FGA_Poss_Prop'],
                          ['T1_2PA_Poss_Prop', 'T2_2PA_Poss_Prop'], ['T1_3PA_Poss_Prop', 'T2_3PA_Poss_Prop'],
                          ['T1_FTA_Poss_Prop', 'T2_FTA_Poss_Prop'], ['T1_FTA_FGA_Rto', 'T2_FTA_FGA_Rto'],
                          ['T1_EFG_Pct', 'T2_EFG_Pct'],
                          ['T1_TS_Pct', 'T2_TS_Pct'], ['T1_OREB_REB_Pct', 'T2_OREB_REB_Pct'],
                          ['T1_DREB_REB_Pct', 'T2_DREB_REB_Pct'],
                          ['T1_TOV_Poss_Pct', 'T2_TOV_Poss_Pct'], ['T1_PF_Poss_Pct', 'T2_PF_Poss_Pct'],
                          ['T2_Poss_Cnt', 'T1_Poss_Cnt'],
                          ['T2_Poss_Sec', 'T1_Poss_Sec'], ['T2_Poss_Sdp', 'T1_Poss_Sdp'],
                          ['T2_FGA_Poss_Prop', 'T1_FGA_Poss_Prop'],
                          ['T2_2PA_Poss_Prop', 'T1_2PA_Poss_Prop'], ['T2_3PA_Poss_Prop', 'T1_3PA_Poss_Prop'],
                          ['T2_FTA_Poss_Prop', 'T1_FTA_Poss_Prop'], ['T2_FTA_FGA_Rto', 'T1_FTA_FGA_Rto'],
                          ['T2_EFG_Pct', 'T1_EFG_Pct'],
                          ['T2_TS_Pct', 'T1_TS_Pct'], ['T2_OREB_REB_Pct', 'T1_OREB_REB_Pct'],
                          ['T2_DREB_REB_Pct', 'T1_DREB_REB_Pct'],
                          ['T2_TOV_Poss_Pct', 'T1_TOV_Poss_Pct'], ['T2_PF_Poss_Pct', 'T1_PF_Poss_Pct']]

            value_name = ['Team', 'Team_Loc', 'Team_sea_g_played', 'Team_B2B', 'PD_Box', 'PD_Poss', 'Off_PTS',
                          'Off_FGM',
                          'Off_FGA', 'Off_FG_Pct', 'Off_2PM', 'Off_2PA', 'Off_2P_Pct', 'Off_3PM', 'Off_3PA',
                          'Off_3P_Pct',
                          'Off_FTM', 'Off_FTA', 'Off_FT_Pct', 'Off_OREB', 'Off_DREB', 'Off_REB', 'Off_AST', 'Off_TOV',
                          'Off_STL', 'Off_BLK', 'Off_PF', 'Def_PTS', 'Def_FGM',
                          'Def_FGA', 'Def_FG_Pct', 'Def_2PM', 'Def_2PA', 'Def_2P_Pct', 'Def_3PM', 'Def_3PA',
                          'Def_3P_Pct',
                          'Def_FTM', 'Def_FTA', 'Def_FT_Pct', 'Def_OREB', 'Def_DREB', 'Def_REB', 'Def_AST', 'Def_TOV',
                          'Def_STL', 'Def_BLK', 'Def_PF', 'Off_Poss_Cnt', 'Off_Poss_Sec', 'Off_Poss_Sdp',
                          'Off_FGA_Poss_Prop',
                          'Off_2PA_Poss_Prop', 'Off_3PA_Poss_Prop', 'Off_FTA_Poss_Prop', 'Off_FTA_FGA_Rto',
                          'Off_EFG_Pct',
                          'Off_TS_Pct', 'Off_OREB_REB_Pct', 'Off_DREB_REB_Pct', 'Off_TOV_Poss_Pct', 'Off_PF_Poss_Pct',
                          'Def_Poss_Cnt', 'Def_Poss_Sec', 'Def_Poss_Sdp', 'Def_FGA_Poss_Prop', 'Def_2PA_Poss_Prop',
                          'Def_3PA_Poss_Prop', 'Def_FTA_Poss_Prop', 'Def_FTA_FGA_Rto', 'Def_EFG_Pct', 'Def_TS_Pct',
                          'Def_OREB_REB_Pct', 'Def_DREB_REB_Pct', 'Def_TOV_Poss_Pct', 'Def_PF_Poss_Pct']

            test = [[x.lower() for x in sub_value_vars] for sub_value_vars in value_vars]

            df_melted = melt.call_multi_melt(df,
                                             [x.lower() for x in id_vars],
                                             [[x.lower() for x in sub_value_vars] for sub_value_vars in value_vars],
                                             [x.lower() for x in value_name]).drop(columns=['variable'])

            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)

            final_df = df_melted[
                ['uuid', 'date', 'season', 'g_type', 'team', 'team_loc', 'team_sea_g_played', 'team_b2b', 'mp',
                 'box_type', 'pd_box', 'pt_box', 'off_pts', 'off_fgm', 'off_fga', 'off_fg_pct', 'off_2pm', 'off_2pa',
                 'off_2p_pct', 'off_3pm', 'off_3pa', 'off_3p_pct', 'off_ftm', 'off_fta', 'off_ft_pct', 'off_oreb',
                 'off_dreb', 'off_reb', 'off_ast', 'off_tov', 'off_stl', 'off_blk', 'off_pf', 'def_pts', 'def_fgm',
                 'def_fga', 'def_fg_pct', 'def_2pm', 'def_2pa', 'def_2p_pct', 'def_3pm', 'def_3pa', 'def_3p_pct',
                 'def_ftm', 'def_fta', 'def_ft_pct', 'def_oreb', 'def_dreb', 'def_reb', 'def_ast', 'def_tov',
                 'def_stl', 'def_blk', 'def_pf', 'pd_poss', 'pt_poss', 'off_poss_cnt', 'off_poss_sec', 'off_poss_sdp',
                 'off_fga_poss_prop', 'off_2pa_poss_prop', 'off_3pa_poss_prop', 'off_fta_poss_prop',
                 'off_fta_fga_rto', 'off_efg_pct', 'off_ts_pct', 'off_oreb_reb_pct', 'off_dreb_reb_pct',
                 'off_tov_poss_pct', 'off_pf_poss_pct', 'def_poss_cnt', 'def_poss_sec', 'def_poss_sdp',
                 'def_fga_poss_prop', 'def_2pa_poss_prop', 'def_3pa_poss_prop', 'def_fta_poss_prop',
                 'def_fta_fga_rto', 'def_efg_pct', 'def_ts_pct', 'def_oreb_reb_pct', 'def_dreb_reb_pct',
                 'def_tov_poss_pct', 'def_pf_poss_pct']]
            final_df.sort_values(by=['uuid', 'box_type'], inplace=True)

            filtered_df = final_df[['uuid', 'team', 'box_type', 'pd_box', 'pt_box', 'pd_poss', 'pt_poss']]
            print(filtered_df)

            fss_obj.build_group('temp_group',
                                1,
                                "temporary feature group",
                                ['uuid', 'date', 'season', 'box_type', 'team'],
                                [],
                                final_df.columns.tolist(),
                                final_df)
            fg_temp = fss_obj.get_group('temp_group', 1)
            query = fg_temp.select_all()
            fss_obj.drop_group('temp_group', 1)
            return query

        except Exception as e:
            logger.error(e)

        finally:
            pass

    def build_view_t1vst2(self, view_name, view_version, description, view_json):
        try:
            logger.info('Getting feature groups details')
            query = hsfs.constructor.query.Query

            for groups in view_json:
                name = groups["name"]
                version = groups["version"]
                features = groups["features"]
                join_sequence = groups["join_sequence"]
                joining_columns = groups["joining_columns"]
                join_type = groups["join_type"]
                fss_obj = fss.FeatureStoreService(self.conf)
                fg_name = fss_obj.get_group(
                    name,
                    version
                )
                filters = ""
                if join_sequence == 1:
                    if groups["filters"] is not str.strip(""):
                        filters = ".filter(" + groups["filters"] + ")"
                    q = "fg_name.select([" + "'{}'".format("','".join(features)) + "])" + filters
                    query = eval(q)
                else:
                    if groups["filters"] is not str.strip(""):
                        filters = ".filter(" + groups["filters"] + ")"
                    q = "query.join(fg_name.select([" + "'{}'".format(
                        "','".join(features)) + "])" + filters + ",on=[" + "'{}'".format(
                        "','".join(joining_columns)) + "],join_type='" + join_type + "')"
                    query = eval(q)

            str_query = query.to_string()
            return query

        except Exception as e:
            logger.error(e)

        finally:
            pass

    def build_view_league(self, main_feature_group, secondary_feature_groups, view_name, view_version, labels,
                          description):
        try:
            logger.info('Getting feature groups details')
            fss_obj = fss.FeatureStoreService(self.conf)
            main_feature_group_handle = fss_obj.get_group(main_feature_group["name"], main_feature_group["version"])
            if len(main_feature_group["filters"]) > 0:
                main_feature_group_handle = main_feature_group_handle.filter(eval(main_feature_group["filters"]))

            query = "main_feature_group_handle.select(main_feature_group['features'])"
            for group in secondary_feature_groups:
                name = group["name"]
                version = group["version"]
                secondary_feature_group_handle = fss_obj.get_group(name, version)
                if len(group["filters"]) > 0:
                    secondary_feature_group_handle = secondary_feature_group_handle.filter(eval(group["filters"]))
                query = query + ".join(secondary_feature_group_handle.select(group['features']), \
                          on=main_feature_group['joining_column']==group['joining_column'], \
                          join_type=group['join_type'])"
            query_string = eval(query)

            fss_obj.build_view(view_name, view_version, description, "", query_string)

        except Exception as e:
            logger.error(e)

        finally:
            pass

    def build_view(self, view_name, view_version, description, view_json):
        try:
            cfs_obj = ComplexFeatureService(self.conf)
            if (view_name == 'team'):
                ##TODO: Implement logic for team view
                pass
                # query = cfs_obj.build_view_team()
                # fss_obj = fss.FeatureStoreService(self.conf)
                # fss_obj.build_view(view_name, view_version, description, "", query)

            elif (view_name == 'league'):
                ##TODO: Implement logic for league view
                pass
                # query = cfs_obj.build_view_league(view_name, view_version, description, view_json)
                # fss_obj = fss.FeatureStoreService(self.conf)
                # fss_obj.build_view(view_name, view_version, description, "", query)

            elif (view_name == 't1vst2'):
                query = cfs_obj.build_view_t1vst2(view_name, view_version, description, view_json)
                fss_obj = fss.FeatureStoreService(self.conf)
                fss_obj.build_view(view_name, view_version, description, "", query)
            else:
                logger.error('Feature view function not found. Please implement the function in '
                             'ComplexFeatureService class.')
        except Exception as e:
            logger.error(e)

        finally:
            pass