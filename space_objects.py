# size: [m, m, m]
# mass: tons
# velocity: m/s
# acceleration: g (9,81 m/s²)
# orientation_velocity:
# orientation_acceleration:
# rotation_velocity: rad/s
# rotation_acceleration: rad/s² ((rad/s)/s)


ships = {'test_ship': {'size': {'length': 600,
                                'height': 100,
                                'width': 100
                                },
                       'mass': 50000,
                       'max_values': {'velocity': 100000,
                                      'acceleration': 500,
                                      'orientation_velocity': 0.5,
                                      'orientation_acceleration': 0.1,
                                      'rotation_velocity': 0.5,
                                      'rotation_acceleration': 0.1
                                      },
                       'weapons': {'broadside': [{'name': 'LaserMkI',
                                                  'amount': 4}],
                                   'bow': [{'name': 'LaserMkI',
                                            'amount': 1}],
                                   'stern': [{'name': 'LaserMkI',
                                              'amount': 1}]
                                   },
                       'shields': {'broadside': 100,
                                   'bow': 0,
                                   'stern': 0,
                                   'vertical': -1
                                   },
                       'armor': {'broadside': 2,
                                 'bow': 4,
                                 'stern': 4,
                                 'inner': 0.1,
                                 'vertical': 0
                                 },
                       'compartment_health': 10
                       }
         }

weapon_systems = {'test': {'type': 'test',
                           'subtype': 'test_subtype',
                           'cycle_time': 42
                           },
                  'test_beam': {'type': 'beam',
                                'subtype': 'test_subtype',
                                'cycle_time': 42,
                                'damage': 42.42
                                },
                  'LaserMkI': {'type': 'beam',
                               'subtype': 'beam_offensive',
                               'cycle_time': 10,
                               'damage': 1
                               },
                  'LaserMkII': {'type': 'beam',
                                'subtype': 'beam_offensive',
                                'cycle_time': 12,
                                'damage': 2
                                },
                  'AntiMissileMkI': {'type': 'rocket_launcher',
                                     'subtype': 'anti_missile',
                                     'cycle_time': 5}
                  }

ordnance = {'test': {'type': 'rocket',
                     'damage': 42},
            'AntiMissileRocketMkI': {'type': 'rocket',
                                     'damage': 1}
            }
