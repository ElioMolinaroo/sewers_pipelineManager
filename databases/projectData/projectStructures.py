struct_assetESMA = {
    'name': 'projectName',
    'children': [
        {'name': '00_management'},
        {'name': '01_external_data'},
        {'name': '02_resource'},
        {
            'name': '03_preprod',
            'children': [
                {
                    'name': '01_scenario',
                    'children': [
                        {'name': 'edit'},
                        {'name': 'publish'}
                    ]
                },
                {
                    'name': '02_storyboom',
                    'children': [
                        {'name': 'edit'},
                        {'name': 'publish'}
                    ]
                },
                {
                    'name': '03_fond_forme',
                    'children': [
                        {'name': 'edit'},
                        {'name': 'publish'}
                    ]
                },
                {
                    'name': '04_lumascript',
                    'children': [
                        {'name': 'edit'},
                        {'name': 'publish'}
                    ]
                },
                {
                    'name': '05_colorscript',
                    'children': [
                        {'name': 'edit'},
                        {'name': 'publish'}
                    ]
                },
                {
                    'name': '06_key_shot',
                    'children': [
                        {'name': 'edit'},
                        {'name': 'publish'}
                    ]
                },
                {'name': '07_concept_design'}
            ]
        },
        {
            'name': '04_workspace',
            'children': [
                {
                    'name': 'houdini',
                    'children': [
                        {'name': 'abc'},
                        {'name': 'audio'},
                        {'name': 'comp'},
                        {'name': 'desk'},
                        {'name': 'flip'},
                        {'name': 'geo'},
                        {'name': 'hdz'},
                        {'name': 'render'},
                        {'name': 'scripts'},
                        {'name': 'sim'},
                        {'name': 'tex'},
                        {'name': 'video'}
                    ]
                },
                {
                    'name': 'maya',
                    'children': [
                        {
                            'name': 'cache',
                            'children': [
                                {'name': 'alembic'},
                                {'name': 'bifrost'},
                                {'name': 'nCache'},
                                {'name': 'particles'}
                            ]
                        },
                        {'name': 'data'},
                        {'name': 'images'},
                        {
                            'name': 'scenes',
                            'children': [
                                {
                                    'name': 'edit',
                                    'children': [
                                        {'name': 'assetLayout'},
                                        {'name': 'dressing'},
                                        {'name': 'groom'},
                                        {'name': 'lookdev'},
                                        {'name': 'modeling'},
                                        {'name': 'rig'}
                                    ]
                                },
                                {
                                    'name': 'publish',
                                    'children': [
                                        {'name': 'assetLayout'},
                                        {'name': 'dressing'},
                                        {'name': 'geo'},
                                        {'name': 'groom'},
                                        {'name': 'lightRig'},
                                        {'name': 'lookdev'},
                                        {'name': 'rig'},
                                        {'name': 'shader'}
                                    ]
                                },
                                {'name': 'shot'}
                            ]
                        },
                        {'name': 'sound'},
                        {
                            'name': 'sourceimages',
                            'children': [
                                {'name': '3dPaintTextures'},
                                {'name': 'environment'},
                                {'name': 'imagePlane'},
                                {'name': 'imageSequence'}
                            ]
                        }
                    ]
                },
                {'name': 'nuke', 'children': [{'name': 'input'}, {'name': 'output'}]},
                {'name': 'paint_2D'},
                {
                    'name': 'paint_3D',
                    'children': [
                        {'name': 'mari'},
                        {'name': 'substance'}
                    ]
                },
                {
                    'name': 'photogrammetry',
                    'children': [
                        {'name': 'input'},
                        {'name': 'output'}
                    ]
                },
                {
                    'name': 'review',
                    'children': [
                        {'name': 'images'},
                        {'name': 'videos'}
                    ]
                },
                {
                    'name': 'sculpt',
                    'children': [
                        {
                            'name': 'zbrush',
                            'children': [
                                {'name': 'input'},
                                {'name': 'output'}
                            ]
                        }
                    ]
                },
                {
                    'name': 'wrap',
                    'children': [
                        {'name': 'input'},
                        {'name': 'output'}
                    ]
                }
            ]
        }
    ]
}
assets_assetESMA = ''
shots_assetESMA = ''

struct_pipelineESMA = {
  "name": "projectName",
  "children": [
    {
      "name": "00_management"
    },
    {
      "name": "01_external_data"
    },
    {
      "name": "02_ressource"
    },
    {
      "name": "03_preprod",
      "children": [
        {
          "name": "01_scenario",
          "children": [
            {
              "name": "edit"
            },
            {
              "name": "publish"
            }
          ]
        },
        {
          "name": "02_storyboom",
          "children": [
            {
              "name": "edit"
            },
            {
              "name": "publish"
            }
          ]
        },
        {
          "name": "03_fond_forme",
          "children": [
            {
              "name": "edit"
            },
            {
              "name": "publish"
            }
          ]
        },
        {
          "name": "04_lumascript",
          "children": [
            {
              "name": "edit"
            },
            {
              "name": "publish"
            }
          ]
        },
        {
          "name": "05_colorscript",
          "children": [
            {
              "name": "edit"
            },
            {
              "name": "publish"
            }
          ]
        },
        {
          "name": "06_key_shot",
          "children": [
            {
              "name": "edit"
            },
            {
              "name": "publish"
            }
          ]
        },
        {
          "name": "07_concept_design"
        }
      ]
    },
    {
      "name": "04_asset",
      "children": [
        {
          "name": "character"
        },
        {
          "name": "FX"
        },
        {
          "name": "prop"
        },
        {
          "name": "set"
        }
      ]
    },
    {
      "name": "05_shot",
      "children": [
        {
          "name": "_credits"
        },
        {
          "name": "_master_camera_"
        },
        {
          "name": "_master_layout"
        }
      ]
    },
    {
      "name": "06_review"
    },
    {
      "name": "07_editing",
      "children": [
        {
          "name": "input_shot"
        },
        {
          "name": "input_sound"
        },
        {
          "name": "output"
        }
      ]
    },
    {
      "name": "08_test"
    },
    {
      "name": "09_print",
      "children": [
        {
          "name": "maya",
          "children": [
            {
              "name": "assets"
            },
            {
              "name": "autosave"
            },
            {
              "name": "cache",
              "children": [
                {
                  "name": "bifrost"
                },
                {
                  "name": "nCache"
                },
                {
                  "name": "particles"
                }
              ]
            },
            {
              "name": "clips"
            },
            {
              "name": "data"
            },
            {
              "name": "images",
              "children": [
                {
                  "name": "edits"
                }
              ]
            },
            {
              "name": "movies"
            },
            {
              "name": "postprod",
              "children": [
                {
                  "name": "input"
                },
                {
                  "name": "output"
                }
              ]
            },
            {
              "name": "renderData",
              "children": [
                {
                  "name": "depth"
                },
                {
                  "name": "fur",
                  "children": [
                    {
                      "name": "furAttrMap"
                    },
                    {
                      "name": "furEqualMap"
                    },
                    {
                      "name": "furFiles"
                    },
                    {
                      "name": "furImages"
                    },
                    {
                      "name": "furShadowMap"
                    }
                  ]
                },
                {
                  "name": "iprImages"
                },
                {
                  "name": "shaders"
                }
              ]
            },
            {
              "name": "renderman"
            },
            {
              "name": "scenes",
              "children": [
                {
                  "name": "backup"
                },
                {
                  "name": "edits"
                }
              ]
            },
            {
              "name": "scripts"
            },
            {
              "name": "sound"
            },
            {
              "name": "sourceimages",
              "children": [
                {
                  "name": "3dPaintTextures"
                },
                {
                  "name": "edits"
                },
                {
                  "name": "environment"
                },
                {
                  "name": "imagePlane"
                },
                {
                  "name": "imageSequence"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "name": "10_jury"
    }
  ]
}
assets_pipelineESMA = './04_asset'
shots_pipelineESMA = './05_shot'
