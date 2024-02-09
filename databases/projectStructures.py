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

struct_pipelineESMA = {'name': 'projectName', 
                       'children': [{'name': '00_management'},
              {'name': '01_external_data'},
              {'name': '02_ressource'},
              {'children': [{'children': [{'name': 'edit'},
                                          {'name': 'publish'}],
                             'name': '01_scenario'},
                            {'children': [{'name': 'edit'},
                                          {'name': 'publish'}],
                             'name': '02_storyboard'},
                            {'children': [{'name': 'edit'},
                                          {'name': 'publish'}],
                             'name': '03_lumascript'},
                            {'children': [{'name': 'edit'},
                                          {'name': 'publish'}],
                             'name': '04_colorscript'},
                            {'children': [{'name': 'edit'},
                                          {'name': 'publish'}],
                             'name': '05_key_shot'},
                            {'name': '06_concept_design'}],
               'name': '03_preprod'},
              {'children': [{'name': 'character'},
                            {'name': 'FX'},
                            {'name': 'item'},
                            {'name': 'prop'},
                            {'name': 'set'}],
               'name': '04_asset'},
              {'children': [{'name': '_credits'},
                            {'name': '_masterCamera'},
                            {'name': '_RLO_roughLayout'},
                            {'name': '_TLO_sequenceLayout'}],
               'name': '05_shot'},
              {'name': '06_review'},
              {'children': [{'name': 'input_shot'},
                            {'name': 'input_sound'},
                            {'name': 'output'}],
               'name': '07_editing'},
              {'name': '08_test'},
              {'children': [{'children': [{'name': 'assets'},
                                          {'name': 'autosave'},
                                          {'children': [{'name': 'bifrost'},
                                                        {'name': 'nCache'},
                                                        {'name': 'particles'}],
                                           'name': 'cache'},
                                          {'name': 'clips'},
                                          {'name': 'data'},
                                          {'children': [{'name': 'edits'}],
                                           'name': 'images'},
                                          {'name': 'movies'},
                                          {'children': [{'name': 'input'},
                                                        {'name': 'output'}],
                                           'name': 'postprod'},
                                          {'children': [{'name': 'depth'},
                                                        {'children': [{'name': 'furAttrMap'},
                                                                      {'name': 'furEqualMap'},
                                                                      {'name': 'furFiles'},
                                                                      {'name': 'furImages'},
                                                                      {'name': 'furShadowMap'}],
                                                         'name': 'fur'},
                                                        {'name': 'iprImages'},
                                                        {'name': 'shaders'}],
                                           'name': 'renderData'},
                                          {'name': 'renderman'},
                                          {'children': [{'name': 'backup'},
                                                        {'name': 'edits'}],
                                           'name': 'scenes'},
                                          {'name': 'scripts'},
                                          {'name': 'sound'},
                                          {'children': [{'name': '3dPaintTextures'},
                                                        {'name': 'edits'},
                                                        {'name': 'environment'},
                                                        {'name': 'imagePlane'},
                                                        {'name': 'imageSequence'}],
                                           'name': 'sourceimages'}],
                             'name': '_template_print'}],
               'name': '09_print'},
              {'name': '10_jury'}]}


assets_pipelineESMA = './04_asset'
shots_pipelineESMA = './05_shot'
