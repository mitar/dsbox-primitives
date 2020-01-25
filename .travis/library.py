from d3m.metadata.problem import TaskKeyword
from template import DSBoxTemplate
from template_steps import TemplateSteps


class DefaultClassificationTemplate(DSBoxTemplate):
    def __init__(self):
        DSBoxTemplate.__init__(self)
        self.template = {
            "name": "default_classification_template",
            "taskSubtype": {TaskKeyword.BINARY.name, TaskKeyword.MULTICLASS.name},
            "taskType": TaskKeyword.CLASSIFICATION.name,
            "runType": "classification",
            "inputType": "table",  # See SEMANTIC_TYPES.keys() for range of values
            "output": "model_step",  # Name of the final step generating the prediction
            "target": "extract_target_step",  # Name of the step generating the ground truth
            "steps": (TemplateSteps.dsbox_generic_steps()
                      + TemplateSteps.dsbox_feature_selector("classification", first_input='data', second_input='target')
                      + [
                          {
                              "name": "model_step",
                              "runtime": {
                                  "cross_validation": 10,
                                  "stratified": True
                              },
                              "primitives": [
                                  {
                                      "primitive":
                                      "d3m.primitives.classification.gradient_boosting.SKlearn",
                                      "hyperparameters":
                                      {
                                          'use_semantic_types': [True],
                                          'return_result': ['new'],
                                          'add_index_columns': [True],
                                          'max_depth': [5],
                                          'learning_rate':[0.1],
                                          'min_samples_leaf': [2],
                                          'min_samples_split': [3],
                                          'n_estimators': [50],
                                         }
                                  }
                              ],
                              "inputs": ["feature_selector_step", "target"]
                          }
                      ])
        }


class DefaultClassificationTemplate2(DSBoxTemplate):
    def __init__(self):
        DSBoxTemplate.__init__(self)
        self.template = {
            "name": "default_classification_template2",
            "taskSubtype": {TaskKeyword.BINARY.name, TaskKeyword.MULTICLASS.name},
            "taskType": TaskKeyword.CLASSIFICATION.name,
            "runType": "classification",
            "inputType": "table",  # See SEMANTIC_TYPES.keys() for range of values
            "output": "model_step",  # Name of the final step generating the prediction
            "target": "extract_target_step",  # Name of the step generating the ground truth
            "steps": (TemplateSteps.dsbox_generic_steps2()
                      + TemplateSteps.dsbox_feature_selector("classification", first_input='data', second_input='target')
                      + [
                          {
                              "name": "model_step",
                              "runtime": {
                                  "cross_validation": 10,
                                  "stratified": True
                              },
                              "primitives": [
                                  {
                                      "primitive":
                                      "d3m.primitives.classification.gradient_boosting.SKlearn",
                                      "hyperparameters":
                                      {
                                          'use_semantic_types': [True],
                                          'return_result': ['new'],
                                          'add_index_columns': [True],
                                          'max_depth': [5],
                                          'learning_rate':[0.1],
                                          'min_samples_leaf': [2],
                                          'min_samples_split': [3],
                                          'n_estimators': [50],
                                         }
                                  }
                              ],
                              "inputs": ["feature_selector_step", "target"]
                          }
                      ])
        }


class DefaultTimeseriesCollectionTemplate(DSBoxTemplate):
    def __init__(self):
        DSBoxTemplate.__init__(self)
        self.template = {
            "name": "Default_timeseries_collection_template",
            "taskType": TaskKeyword.CLASSIFICATION.name,
            "taskSubtype": {TaskKeyword.BINARY.name, TaskKeyword.MULTICLASS.name},
            "runType": "timeseries",
            "inputType": {"timeseries", "table"},  # See SEMANTIC_TYPES.keys() for range of values
            "output": "random_forest_step",  # Name of the final step generating the prediction
            "target": "extract_target_step",  # Name of the step generating the ground truth
            "steps": [

                {
                    "name": "denormalize_step",
                    "primitives": ["d3m.primitives.data_transformation.denormalize.Common"],
                    "inputs": ["template_input"]
                },
                {
                    "name": "to_dataframe_step",
                    "primitives": ["d3m.primitives.data_transformation.dataset_to_dataframe.Common"],
                    "inputs": ["denormalize_step"]
                },
                # read Y value
                {
                    "name": "pre_extract_target_step",
                    "primitives": [{
                        "primitive": "d3m.primitives.data_transformation.extract_columns_by_semantic_types.Common",
                        "hyperparameters":
                            {'semantic_types': ('https://metadata.datadrivendiscovery.org/types/TrueTarget',),
                             'use_columns': (),
                             'exclude_columns': ()
                             }
                    }],
                    "inputs": ["to_dataframe_step"]
                },
                {
                    "name": "extract_target_step",
                    "primitives": [{
                        "primitive": "d3m.primitives.data_transformation.to_numeric.DSBOX",
                        "hyperparameters": {
                            "drop_non_numeric_columns": [False]
                        }
                    }],
                    "inputs": ["pre_extract_target_step"]
                },
                # {
                #     "name": "column_parser_step",
                #     "primitives": ["d3m.primitives.data_transformation.column_parser.DataFrameCommon"],
                #     "inputs": ["extract_target_step"]
                # },

                # read X value
                {
                    "name": "timeseries_to_list_step",
                    "primitives": ["d3m.primitives.data_preprocessing.time_series_to_list.DSBOX"],
                    "inputs": ["to_dataframe_step"]
                },

                {
                    "name": "random_projection_step",
                    "primitives": [
                        {
                            "primitive": "d3m.primitives.feature_extraction.random_projection_timeseries_featurization.DSBOX",
                            "hyperparameters":{
                                'generate_metadata':[True],
                            }
                        }
                    ],
                    "inputs": ["timeseries_to_list_step"]
                },

                {
                    "name": "random_forest_step",
                    "primitives": [
                        {
                            "primitive": "d3m.primitives.classification.random_forest.SKlearn",
                            "hyperparameters": {
                                'add_index_columns': [True],
                                'use_semantic_types':[True],
                            }
                        }
                    ],
                    "inputs": ["random_projection_step", "extract_target_step"]
                },
            ]
        }


class DefaultRegressionTemplate(DSBoxTemplate):
    def __init__(self):
        DSBoxTemplate.__init__(self)
        self.template = {
            "name": "default_regression_template",
            "taskSubtype": {TaskKeyword.UNIVARIATE.name, TaskKeyword.MULTIVARIATE.name},
            "taskType": TaskKeyword.REGRESSION.name,
            "runType": "regression",
            "inputType": "table",  # See SEMANTIC_TYPES.keys() for range of values
            "output": "model_step",  # Name of the final step generating the prediction
            "target": "extract_target_step",  # Name of the step generating the ground truth
            "steps": TemplateSteps.dsbox_generic_steps() + [
                {
                    "name": "model_step",
                    "runtime": {
                        "test_validation": 5,
                        "stratified": False
                    },
                    "primitives": [
                        {
                            "primitive":
                                "d3m.primitives.regression.gradient_boosting.SKlearn",
                            "hyperparameters":
                                {
                                    'max_depth': [2, 3, 4, 5],
                                    'n_estimators': [100, 130, 165, 200],
                                    'learning_rate': [0.1, 0.23, 0.34, 0.5],
                                    'min_samples_split': [2, 3],
                                    'min_samples_leaf': [1, 2],
                                    'add_index_columns': [True],
                                    'use_semantic_types':[True],
                                }
                        },
                        {
                            "primitive":
                                "d3m.primitives.regression.extra_trees.SKlearn",
                            "hyperparameters":
                                {
                                    'bootstrap': [True, False],
                                    'max_depth': [15, 30, None],
                                    'min_samples_leaf': [1, 2, 4],
                                    'min_samples_split': [2, 5, 10],
                                    'max_features': ['auto', 'sqrt'],
                                    'n_estimators': [10, 50, 100],
                                    'add_index_columns': [True],
                                    'use_semantic_types':[True],
                                }
                        },
                        {
                            "primitive":
                                "d3m.primitives.regression.random_forest.SKlearn",
                            "hyperparameters":
                                {
                                    'bootstrap': [True, False],
                                    'max_depth': [15, 30, None],
                                    'min_samples_leaf': [1, 2, 4],
                                    'min_samples_split': [2, 5, 10],
                                    'max_features': ['auto', 'sqrt'],
                                    'n_estimators': [10, 50, 100],
                                    'add_index_columns': [True],
                                    'use_semantic_types':[True],
                                }
                        },
                    ],
                    "inputs": ["data", "target"]
                }
            ]
        }


class DefaultRegressionTemplate2(DSBoxTemplate):
    def __init__(self):
        DSBoxTemplate.__init__(self)
        self.template = {
            "name": "default_regression_template2",
            "taskSubtype": {TaskKeyword.UNIVARIATE.name, TaskKeyword.MULTIVARIATE.name},
            "taskType": TaskKeyword.REGRESSION.name,
            "runType": "regression",
            "inputType": "table",  # See SEMANTIC_TYPES.keys() for range of values
            "output": "model_step",  # Name of the final step generating the prediction
            "target": "extract_target_step",  # Name of the step generating the ground truth
            "steps": TemplateSteps.dsbox_generic_steps3() + [
                {
                    "name": "model_step",
                    "runtime": {
                        "test_validation": 5,
                        "stratified": False
                    },
                    "primitives": [
                        {
                            "primitive":
                                "d3m.primitives.regression.gradient_boosting.SKlearn",
                            "hyperparameters":
                                {
                                    'max_depth': [2, 3, 4, 5],
                                    'n_estimators': [100, 130, 165, 200],
                                    'learning_rate': [0.1, 0.23, 0.34, 0.5],
                                    'min_samples_split': [2, 3],
                                    'min_samples_leaf': [1, 2],
                                    'add_index_columns': [True],
                                    'use_semantic_types':[True],
                                }
                        },
                        {
                            "primitive":
                                "d3m.primitives.regression.extra_trees.SKlearn",
                            "hyperparameters":
                                {
                                    'bootstrap': [True, False],
                                    'max_depth': [15, 30, None],
                                    'min_samples_leaf': [1, 2, 4],
                                    'min_samples_split': [2, 5, 10],
                                    'max_features': ['auto', 'sqrt'],
                                    'n_estimators': [10, 50, 100],
                                    'add_index_columns': [True],
                                    'use_semantic_types':[True],
                                }
                        },
                        {
                            "primitive":
                                "d3m.primitives.regression.random_forest.SKlearn",
                            "hyperparameters":
                                {
                                    'bootstrap': [True, False],
                                    'max_depth': [15, 30, None],
                                    'min_samples_leaf': [1, 2, 4],
                                    'min_samples_split': [2, 5, 10],
                                    'max_features': ['auto', 'sqrt'],
                                    'n_estimators': [10, 50, 100],
                                    'add_index_columns': [True],
                                    'use_semantic_types':[True],
                                }
                        },
                    ],
                    "inputs": ["data", "target"]
                }
            ]
        }


class VotingTemplate(DSBoxTemplate):
    def __init__(self):
        DSBoxTemplate.__init__(self)
        self.template = {
            "name": "default_classification_template",
            "taskSubtype": {TaskKeyword.BINARY.name, TaskKeyword.MULTICLASS.name},
            "taskType": TaskKeyword.CLASSIFICATION.name,
            "runType": "voting_classification",
            "inputType": "table",  # See SEMANTIC_TYPES.keys() for range of values
            "output": "model_step",  # Name of the final step generating the prediction
            "target": "extract_target_step",  # Name of the step generating the ground truth
            "steps": (TemplateSteps.dsbox_generic_steps()
                      + TemplateSteps.dsbox_feature_selector("classification", first_input='data', second_input='target')
                      + [
                          {
                              "name": "model_substep_1",
                              "primitives": [
                                  {
                                      "primitive": "d3m.primitives.classification.linear_discriminant_analysis.SKlearn",
                                      "hyperparameters": {
                                          'use_semantic_types': [True],
                                          'return_result': ['new'],
                                          'add_index_columns': [True],
                                      }
                                  }],
                              "inputs": ["feature_selector_step", "target"]
                          },
                          {
                              "name": "model_substep_2",
                              "primitives": [
                                  {
                                      "primitive": "d3m.primitives.classification.nearest_centroid.SKlearn",
                                      "hyperparameters": {
                                          'use_semantic_types': [True],
                                          'return_result': ['new'],
                                          'add_index_columns': [True],
                                      }
                                  }],
                              "inputs": ["feature_selector_step", "target"]
                          },
                          {
                              "name": "model_substep_3",
                              "primitives": [
                                  {
                                      "primitive": "d3m.primitives.classification.logistic_regression.SKlearn",
                                      "hyperparameters": {
                                          'use_semantic_types': [True],
                                          'return_result': ['new'],
                                          'add_index_columns': [True],
                                      }
                                  }],
                              "inputs": ["feature_selector_step", "target"]
                          },
                          {
                              "name": "vertical_concat",
                              "primitives": [
                                  {
                                      "primitive": "d3m.primitives.data_preprocessing.vertical_concatenate.DSBOX",
                                      "hyperparameters": {}
                                  }],
                              "inputs": [["model_substep_1", "model_substep_2", "model_substep_3"]]
                          },
                          {
                              "name": "model_step",
                              "primitives": [
                                  {
                                      "primitive": "d3m.primitives.classification.ensemble_voting.DSBOX",
                                      "hyperparameters": {}
                                  }],
                              "inputs": ["vertical_concat", "target"]
                          }
                      ])
        }

class HorizontalVotingTemplate(DSBoxTemplate):
    'Horizontal Voting Template'
    def __init__(self):
        DSBoxTemplate.__init__(self)
        self.template = {
            "name": "horizontal_voting_template",
            "taskSubtype": {TaskKeyword.BINARY.name, TaskKeyword.MULTICLASS.name},
            "taskType": TaskKeyword.CLASSIFICATION.name,
            "runType": "voting_classification",
            "inputType": "table",  # See SEMANTIC_TYPES.keys() for range of values
            "output": "model_step",  # Name of the final step generating the prediction
            "target": "target",  # Name of the step generating the ground truth
            "steps": (TemplateSteps.dsbox_generic_steps()
                      + TemplateSteps.dsbox_feature_selector("classification", first_input='data', second_input='target')
                      + [
                          {
                              "name": "model_substep_1",
                              "primitives": [
                                  {
                                      "primitive": "d3m.primitives.classification.linear_discriminant_analysis.SKlearn",
                                      "hyperparameters": {
                                          'use_semantic_types': [True],
                                          'return_result': ['new'],
                                          'add_index_columns': [True],
                                      }
                                  }],
                              "inputs": ["feature_selector_step", "target"]
                          },
                          {
                              "name": "model_substep_2",
                              "primitives": [
                                  {
                                      "primitive": "d3m.primitives.classification.nearest_centroid.SKlearn",
                                      "hyperparameters": {
                                          'use_semantic_types': [True],
                                          'return_result': ['new'],
                                          'add_index_columns': [True],
                                      }
                                  }],
                              "inputs": ["feature_selector_step", "target"]
                          },
                          {
                              "name": "model_substep_3",
                              "primitives": [
                                  {
                                      "primitive": "d3m.primitives.classification.logistic_regression.SKlearn",
                                      "hyperparameters": {
                                          'use_semantic_types': [True],
                                          'return_result': ['new'],
                                          'add_index_columns': [True],
                                      }
                                  }],
                              "inputs": ["feature_selector_step", "target"]
                          },
                          {
                              "name": "horizontal_concat",
                              "primitives": [
                                  {
                                      "primitive": "d3m.primitives.data_preprocessing.horizontal_concat.DSBOX",
                                      "hyperparameters": {}
                                  }],
                              "inputs": [["feature_selector_step", "model_substep_1", "model_substep_2", "model_substep_3"]]
                          },
                          {
                              "name": "to_attribute",
                              "primitives": [
                                  {
                                      "primitive": "d3m.primitives.data_transformation.replace_semantic_types.Common",
                                      "hyperparameters": {
                                          'from_semantic_types': [[
                                              "https://metadata.datadrivendiscovery.org/types/Target",
                                              "https://metadata.datadrivendiscovery.org/types/PredictedTarget"
                                          ]],
                                          'to_semantic_types': [[
                                              "https://metadata.datadrivendiscovery.org/types/Attribute"
                                          ]],
                                          'match_logic': ['any'],
                                      }
                                  }
                              ],
                              "inputs": ["horizontal_concat"]
                          },
                          {
                              "name": "encode_new_columns",
                              "primitives": ["d3m.primitives.data_preprocessing.encoder.DSBOX"],
                              "inputs": ["to_attribute"]
                          },
                          {
                              "name": "model_step",
                              "primitives": [
                                  {
                                      "primitive": "d3m.primitives.classification.random_forest.SKlearn",
                                      "hyperparameters": {
                                          'add_index_columns': [True],
                                          'use_semantic_types':[True],
                                      }
                                  }
                              ],
                              "inputs": ["encode_new_columns", "target"]
                          }
                      ])
        }

class TA1ImageProcessingRegressionTemplate(DSBoxTemplate):
    def __init__(self):
        DSBoxTemplate.__init__(self)
        self.template = {
            "name": "TA1ImageProcessingRegressionTemplate",
            "taskType": TaskKeyword.REGRESSION.name,
            "runType": "image_regression",
            # See TaskKeyword, range include 'CLASSIFICATION', 'CLUSTERING', 'COLLABORATIVE_FILTERING', 'COMMUNITY_DETECTION', 'GRAPH_CLUSTERING', 'GRAPH_MATCHING', 'LINK_PREDICTION', 'REGRESSION', 'TIME_SERIES', 'VERTEX_NOMINATION'
            "taskSubtype": {TaskKeyword.UNIVARIATE.name, TaskKeyword.MULTIVARIATE.name},
            "inputType": "image",  # See SEMANTIC_TYPES.keys() for range of values
            "output": "regressor_step",  # Name of the final step generating the prediction
            "target": "extract_target_step",  # Name of the step generating the ground truth
            "steps": [
                {
                    "name": "denormalize_step",
                    "primitives": ["d3m.primitives.data_transformation.denormalize.Common"],
                    "inputs": ["template_input"]
                },
                {
                    "name": "to_dataframe_step",
                    "primitives": ["d3m.primitives.data_transformation.dataset_to_dataframe.Common"],
                    "inputs": ["denormalize_step"]
                },
                # read Y value
                {
                    "name": "pre_extract_target_step",
                    "primitives": [{
                        "primitive": "d3m.primitives.data_transformation.extract_columns_by_semantic_types.Common",
                        "hyperparameters":
                            {'semantic_types': ('https://metadata.datadrivendiscovery.org/types/TrueTarget',),
                             'use_columns': (),
                             'exclude_columns': ()
                             }
                    }],
                    "inputs": ["to_dataframe_step"]
                },
                {
                    "name": "extract_target_step",
                    "primitives": [{
                        "primitive": "d3m.primitives.data_transformation.to_numeric.DSBOX",
                        "hyperparameters": {
                            "drop_non_numeric_columns": [False]
                        }
                    }],
                    "inputs": ["pre_extract_target_step"]
                },
                {
                    "name": "dataframe_to_tensor",
                    "primitives": ["d3m.primitives.data_preprocessing.dataframe_to_tensor.DSBOX"],
                    "inputs": ["to_dataframe_step"]
                },
                {
                    "name": "feature_extraction",
                    "primitives": [
                        {
                            "primitive": "d3m.primitives.feature_extraction.resnet50_image_feature.DSBOX",
                            "hyperparameters": {
                                'generate_metadata': [True]
                            }
                        }
                    ],
                    "inputs": ["dataframe_to_tensor"]
                },
                {
                    "name": "PCA_step",
                    "primitives": [
                        {
                            "primitive": "d3m.primitives.feature_extraction.pca.SKlearn",
                            "hyperparameters": {
                                'add_index_columns': [True],
                                'use_semantic_types': [True]
                            }
                        }
                    ],
                    "inputs": ["feature_extraction"]
                },
                {
                    "name": "regressor_step",
                    "primitives": [
                        {
                            "primitive": "d3m.primitives.regression.random_forest.SKlearn",
                            "hyperparameters": {
                                'add_index_columns': [True],
                            }
                        }
                    ],
                    "inputs": ["PCA_step", "extract_target_step"]
                },
            ]
        }


class TA1ImageProcessingRegressionTemplate2(DSBoxTemplate):
    def __init__(self):
        DSBoxTemplate.__init__(self)
        self.template = {
            "name": "TA1ImageProcessingRegressionTemplate2",
            "taskType": TaskKeyword.REGRESSION.name,
            "runType": "image_regression",
            # See TaskKeyword, range include 'CLASSIFICATION', 'CLUSTERING', 'COLLABORATIVE_FILTERING', 'COMMUNITY_DETECTION', 'GRAPH_CLUSTERING', 'GRAPH_MATCHING', 'LINK_PREDICTION', 'REGRESSION', 'TIME_SERIES', 'VERTEX_NOMINATION'
            "taskSubtype": {TaskKeyword.UNIVARIATE.name, TaskKeyword.MULTIVARIATE.name},
            "inputType": "image",  # See SEMANTIC_TYPES.keys() for range of values
            "output": "regressor_step",  # Name of the final step generating the prediction
            "target": "extract_target_step",  # Name of the step generating the ground truth
            "steps": [
                {
                    "name": "denormalize_step",
                    "primitives": ["d3m.primitives.data_transformation.denormalize.Common"],
                    "inputs": ["template_input"]
                },
                {
                    "name": "to_dataframe_step",
                    "primitives": ["d3m.primitives.data_transformation.dataset_to_dataframe.Common"],
                    "inputs": ["denormalize_step"]
                },
                # read Y value
                {
                    "name": "pre_extract_target_step",
                    "primitives": [{
                        "primitive": "d3m.primitives.data_transformation.extract_columns_by_semantic_types.Common",
                        "hyperparameters":
                            {'semantic_types': ('https://metadata.datadrivendiscovery.org/types/TrueTarget',),
                             'use_columns': (),
                             'exclude_columns': ()
                             }
                    }],
                    "inputs": ["to_dataframe_step"]
                },
                {
                    "name": "extract_target_step",
                    "primitives": [{
                        "primitive": "d3m.primitives.data_transformation.to_numeric.DSBOX",
                        "hyperparameters": {
                            "drop_non_numeric_columns": [False]
                        }
                    }],
                    "inputs": ["pre_extract_target_step"]
                },
                {
                    "name": "dataframe_to_tensor",
                    "primitives": ["d3m.primitives.data_preprocessing.dataframe_to_tensor.DSBOX"],
                    "inputs": ["to_dataframe_step"]
                },
                {
                    "name": "feature_extraction",
                    "primitives": [
                        {
                            "primitive": "d3m.primitives.feature_extraction.vgg16_image_feature.DSBOX",
                            "hyperparameters": {
                                'generate_metadata': [True]
                            }
                        }
                    ],
                    "inputs": ["dataframe_to_tensor"]
                },
                {
                    "name": "PCA_step",
                    "primitives": [
                        {
                            "primitive": "d3m.primitives.feature_extraction.pca.SKlearn",
                            "hyperparameters": {
                                'add_index_columns': [True],
                                'use_semantic_types': [True]
                            }
                        }
                    ],
                    "inputs": ["feature_extraction"]
                },
                {
                    "name": "regressor_step",
                    "primitives": [
                        {
                            "primitive": "d3m.primitives.regression.random_forest.SKlearn",
                            "hyperparameters": {
                                'add_index_columns': [True],
                            }
                        }
                    ],
                    "inputs": ["PCA_step", "extract_target_step"]
                },
            ]
        }


class ARIMATemplate(DSBoxTemplate):
    def __init__(self):
        DSBoxTemplate.__init__(self)
        self.template = {
            "name": "ARIMA_Template",
            "taskType": TaskKeyword.TIME_SERIES.name,
            "runType": "time_series_forecasting",
            "taskSubtype": "NONE",
            "inputType": {"table", "timeseries"},  # See SEMANTIC_TYPES.keys() for range of values
            "output": "ARIMA_step",  # Name of the final step generating the prediction
            "target": "extract_target_step",  # Name of the step generating the ground truth
            "steps": [
                {
                    "name": "denormalize_step",
                    "primitives": ["d3m.primitives.data_transformation.denormalize.Common"],
                    "inputs": ["template_input"]
                },
                {
                    "name": "to_dataframe_step",
                    "primitives": ["d3m.primitives.data_transformation.dataset_to_dataframe.Common"],
                    "inputs": ["template_input"]
                },
                {
                    "name": "parser_step",
                    "primitives": [{
                        "primitive": "d3m.primitives.data_transformation.column_parser.Common",
                        "hyperparameters": {
                            "parse_semantic_types": [('http://schema.org/Boolean', 'http://schema.org/Integer', 'http://schema.org/Float', 'https://metadata.datadrivendiscovery.org/types/FloatVector'),]
                        }
                    }],
                    "inputs": ["to_dataframe_step"]
                },

                # read Y value
                {
                    "name": "extract_target_step",
                    "primitives": [{
                        "primitive": "d3m.primitives.data_transformation.extract_columns_by_semantic_types.Common",
                        "hyperparameters":
                            {
                             'semantic_types': ('https://metadata.datadrivendiscovery.org/types/TrueTarget',),
                             'use_columns': (),
                             'exclude_columns': ()
                            }
                    }],
                    "inputs": ["parser_step"]
                },

                {
                    "name": "extract_attribute_step",
                    "primitives": [{
                        "primitive": "d3m.primitives.data_transformation.extract_columns_by_semantic_types.Common",
                        "hyperparameters":
                            {
                                'semantic_types': ('https://metadata.datadrivendiscovery.org/types/PrimaryKey',
                                                   'https://metadata.datadrivendiscovery.org/types/TrueTarget',
                                                   'https://metadata.datadrivendiscovery.org/types/Attribute',),
                                'use_columns': (),
                                'exclude_columns': ()
                            }
                    }],
                    "inputs": ["parser_step"]
                },
                # {
                #     "name": "extract_attribute_step",
                #     "primitives": ["d3m.primitives.data_transformation.to_numeric.DSBOX"],
                #     "inputs": ["pre_extract_attribute_step"]
                # },
                {
                    "name": "ARIMA_step",
                    "primitives": [
                        {
                            "primitive": "d3m.primitives.time_series_forecasting.arima.DSBOX",
                            "hyperparameters": {
                                "take_log": [(False)],
                                "auto": [(True)]
                            }
                        }
                    ], # can add tuning parameters like: auto-fit, take_log, etc
                    "inputs": ["extract_attribute_step", "extract_target_step"]
                },
            ]
        }


class DefaultObjectDetectionTemplate(DSBoxTemplate):
    def __init__(self):
        DSBoxTemplate.__init__(self)
        self.template = {
            "name": "DefaultObjectDetectionTemplate",
            "taskType": TaskKeyword.OBJECT_DETECTION.name,
            "runType": "object_detection",
            "taskSubtype": "NONE",
            "inputType": {"table", "image"},  # See SEMANTIC_TYPES.keys() for range of values
            "output": "model_step",  # Name of the final step generating the prediction
            "target": "extract_target_step",  # Name of the step generating the ground truth
            "steps": [
                {
                    "name": "denormalize_step",
                    "primitives": ["d3m.primitives.data_transformation.denormalize.Common"],
                    "inputs": ["template_input"]
                },
                {
                    "name": "to_dataframe_step",#step 1
                    "primitives": ["d3m.primitives.data_transformation.dataset_to_dataframe.Common"],
                    "inputs": ["denormalize_step"]
                },
                # read X value
                {
                    "name": "extract_file_step",#step 2
                    "primitives": [{
                        "primitive": "d3m.primitives.data_transformation.extract_columns_by_semantic_types.Common",
                        "hyperparameters":
                            {
                                'semantic_types': (
                                    'https://metadata.datadrivendiscovery.org/types/PrimaryMultiKey',
                                    'https://metadata.datadrivendiscovery.org/types/FileName',),
                                'use_columns': (),
                                'exclude_columns': ()
                            }
                    }],
                    "inputs": ["to_dataframe_step"]
                },
                {
                    "name": "extract_target_step",# step 3
                    "primitives": [{
                        "primitive": "d3m.primitives.data_transformation.extract_columns_by_semantic_types.Common",
                        "hyperparameters":
                            {
                                'semantic_types': (
                                    'https://metadata.datadrivendiscovery.org/types/TrueTarget',),
                                'use_columns': (),
                                'exclude_columns': ()
                            }
                    }],
                    "inputs": ["to_dataframe_step"]
                },
                {
                    "name": "model_step", # step 4
                    "primitives": [
                        {
                            "primitive": "d3m.primitives.feature_extraction.yolo.DSBOX",
                            "hyperparameters": {
                            # "use_fitted_weight": [(False)],
                            # "epochs": [(30)]
                            }
                        }
                    ],
                    "inputs": ["extract_file_step", "extract_target_step"]
                },
            ]
        }


class DefaultVideoClassificationTemplate(DSBoxTemplate):
    def __init__(self):
        DSBoxTemplate.__init__(self)
        self.template = {
            "name": "DefaultVideoClassificationTemplate",
            "taskType": TaskKeyword.CLASSIFICATION.name,
            "taskSubtype": TaskKeyword.MULTICLASS.name,
            "runType": "video_classification",
            "inputType": "video",
            "output": "model_step",  # Name of the final step generating the prediction
            "target": "extract_target_step",  # Name of the step generating the ground truth
            "steps": [
                {
                    "name": "denormalize_step",
                    "primitives": ["d3m.primitives.data_transformation.denormalize.Common"],
                    "inputs": ["template_input"]
                },
                {
                    "name": "to_dataframe_step",#step 1
                    "primitives": ["d3m.primitives.data_transformation.dataset_to_dataframe.Common"],
                    "inputs": ["denormalize_step"]
                },
                # read X value
                {
                    "name": "extract_file_step",#step 2
                    "primitives": [{
                        "primitive": "d3m.primitives.data_transformation.extract_columns_by_semantic_types.Common",
                        "hyperparameters":
                            {
                                'semantic_types': (
                                    'https://metadata.datadrivendiscovery.org/types/PrimaryKey',
                                    'https://metadata.datadrivendiscovery.org/types/FileName',),
                                'use_columns': (),
                                'exclude_columns': ()
                            }
                    }],
                    "inputs": ["to_dataframe_step"]
                },
                {
                    "name": "extract_target_step",# step 3
                    "primitives": [{
                        "primitive": "d3m.primitives.data_transformation.extract_columns_by_semantic_types.Common",
                        "hyperparameters":
                            {
                                'semantic_types': (
                                    'https://metadata.datadrivendiscovery.org/types/TrueTarget',),
                                'use_columns': (),
                                'exclude_columns': ()
                            }
                    }],
                    "inputs": ["to_dataframe_step"]
                },
                {
                    "name": "video_reader",#step 4
                    "primitives": ["d3m.primitives.data_preprocessing.video_reader.Common"],
                    "inputs": ["extract_file_step"]
                },
                {
                    "name": "video_feature_extract",#step 5
                    "primitives": [
                            {
                                "primitive": "d3m.primitives.feature_extraction.inceptionV3_image_feature.DSBOX",
                                "hyperparameters": {
                                    "use_limitation":[(True),],
                                }
                            }

                        ],
                    "inputs": ["video_reader"]
                },
                {
                    "name": "model_step", # step 6
                    "primitives": [
                        {
                            "primitive": "d3m.primitives.classification.lstm.DSBOX",
                            "hyperparameters": {
                                "LSTM_units":[512],
                                "epochs":[50],
                            }
                        }
                    ],
                    "inputs": ["video_feature_extract", "extract_target_step"]
                },
            ]
        }


class UU3TestTemplate(DSBoxTemplate):
    def __init__(self):
        DSBoxTemplate.__init__(self)
        self.template = {
            "name": "UU3_Test_Template",
            "taskSubtype": {TaskKeyword.UNIVARIATE.name, TaskKeyword.MULTIVARIATE.name},
            "taskType": TaskKeyword.REGRESSION.name,
            "inputType": "table",
            "runType": "multitable_dataset",
            "output": "construct_prediction_step",  # Name of the final step generating the prediction
            "target": "extract_target_step",  # Name of the step generating the ground truth
            "steps": [
                # {
                #     "name": "denormalize_step",
                #     "primitives": ["d3m.primitives.data_transformation.denormalize.Common"],
                #     "inputs": ["template_input"]
                # },
                {
                    "name": "multi_table_processing_step",
                    "primitives": ["d3m.primitives.feature_extraction.multitable_featurization.DSBOX"],
                    "inputs": ["template_input"]
                },
                # {
                #     "name": "to_dataframe_step",
                #     "primitives": ["d3m.primitives.data_transformation.dataset_to_dataframe.Common"],
                #     "inputs": ["multi_table_processing_step"]
                # },
                {
                    "name": "common_profiler_step",
                    "primitives": ["d3m.primitives.schema_discovery.profiler.Common"],
                    "inputs": ["multi_table_processing_step"]
                },
                {
                    "name": "extract_attribute_step",
                    "primitives": [{
                        "primitive": "d3m.primitives.data_transformation.extract_columns_by_semantic_types.Common",
                        "hyperparameters":
                            {
                                'semantic_types': (
                                    'https://metadata.datadrivendiscovery.org/types/PrimaryKey',
                                    'https://metadata.datadrivendiscovery.org/types/Attribute',),
                                'use_columns': (),
                                'exclude_columns': ()
                            }
                    }],
                    "inputs": ["common_profiler_step"]
                },
                {
                    "name": "extract_target_step",
                    "primitives": [{
                        "primitive": "d3m.primitives.data_transformation.extract_columns_by_semantic_types.Common",
                        "hyperparameters":
                            {
                                'semantic_types': ('https://metadata.datadrivendiscovery.org/types/TrueTarget',),
                                'use_columns': (),
                                'exclude_columns': ()
                            }
                    }],
                    "inputs": ["multi_table_processing_step"]
                },
                {
                    "name": "encode1_step",
                    "primitives": ["d3m.primitives.data_preprocessing.unary_encoder.DSBOX"],
                    "inputs": ["extract_attribute_step"]
                },
                {
                    "name": "encode2_step",
                    "primitives": ["d3m.primitives.data_preprocessing.encoder.DSBOX"],
                    "inputs": ["encode1_step"]
                },
                {
                    "name": "to_numeric_step",
                    "primitives": ["d3m.primitives.data_transformation.to_numeric.DSBOX"],
                    "inputs":["encode2_step"],
                },
                {
                    "name": "impute_step",
                    "primitives": ["d3m.primitives.data_preprocessing.mean_imputation.DSBOX"],
                    "inputs": ["to_numeric_step"]
                },
                {
                    "name": "model_step",
                    "primitives": [{
                        "primitive": "d3m.primitives.regression.random_forest.SKlearn",
                        "hyperparameters":
                            {
                              'use_semantic_types': [True],
                              'return_result': ['new'],
                              'add_index_columns': [True],
                            }
                    }
                    ],
                    "inputs": ["impute_step", "extract_target_step"]
                },
                {
                  "name": "construct_prediction_step",
                    "primitives": ["d3m.primitives.data_transformation.construct_predictions.Common"],
                    "inputs": ["model_step", "common_profiler_step"]
                }
            ]
        }
