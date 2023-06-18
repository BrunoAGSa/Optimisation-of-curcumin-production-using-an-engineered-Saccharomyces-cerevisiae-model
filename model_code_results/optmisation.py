import time
from builtins import print
from mewpy.util.constants import EAConstants
from mewpy import solvers
from mewpy.optimization import EA
from mewpy.optimization import set_default_engine
from mewpy.optimization.evaluation import BPCY, WYIELD, ModificationType
from mewpy.problems import GOUProblem
from mewpy.simulation import get_simulator, SimulationMethod
from mewpy.util.constants import EAConstants
from mewpy.util.io import population_to_csv
from reframed.io.sbml import load_cbmodel
from cobra.io import read_sbml_model, validate_sbml_model
import warnings

def main(model_filename,
         biomass_id='r_4041',
         product_id='EX_curcumin',
         env_conditions=None):
    if env_conditions is None:
        return

    warnings.filterwarnings("ignore")

    print('Loading model...')
    model = read_sbml_model(model_filename)
    print('Model loaded!')

    print('Setting model objective...')
    model.objective = biomass_id
    print('Model objective set!')

    s = solvers.get_default_solver()
    print('Default solver to be used: ' + str(s))



    for envcond in env_conditions:
        try:
            startTime=time.strftime('%d-%m-%Y__%H_%M_%S')
            print(startTime)
            print(f'Starting with envcond: {envcond}')
            carbon_source = next(iter(envcond))
            print('Setting evaluation functions...')
            evaluator_1 = WYIELD(biomass_id, product_id)
            evaluator_2 = BPCY(biomass_id,
                               product_id,
                               uptake=carbon_source,
                               method=SimulationMethod.pFBA)
            evaluator_3 = ModificationType()
            print('Evaluation functions set!')

            print('Setting the GOUProblem...')
            solution = {'YPR060C': 32, 'YBR249C': 32, 'YDR127W': 32, 'YGL148W': 32, 'YDR035W': 32, 'YBR166C': 32, 'YLR134W': 0, 'YDR380W': 0}
            
            # The reaction up and down regulation optimization problem
            problem = GOUProblem(model,
                                 fevaluation=[evaluator_2,
                                              evaluator_1,
                                              evaluator_3
                                              ],
                                 envcond=envcond,
                                 candidate_min_size=2,
                                 candidate_max_size=8,
                                 partial_solution=solution)
            print('GOUProblem set!')

            # validate whether product is achievable
            res = problem.simulate(objective={product_id:1})
            if res.objective_value < 10E-6:
                continue
            print(res)

            print('Flux simulation complete!')

            model.objective = biomass_id

            print('Starting optimization...')

            ea = EA(problem, max_generations=500)

            ea.run(simplify=False)
            print('Optimization complete!')

            endTime = time.strftime('%d-%m-%Y__%H_%M_%S')
            
            print(endTime)

            print('Writing the results...')
            filename = './results/results_'+startTime+'_'+endTime
            for key, value in envcond.items():
                filename += f'{key}_{value}'
            filename += '.csv'
            df=ea.dataframe()
            df.to_csv(filename)
            
            print('End!')

        except BaseException as ex:
            print('Exception occurred!')
            print(ex)


if __name__ == '__main__':
    PRODUCT_ID = 'EX_curcumin'
    model_f = 'yeast-7-GEM_curcumin.xml'
    
    BIOMASS_ID = 'r_4041'
    GLC = 'r_1714'
    #XYL = 'r_1718'
    #GLY = 'r_1808'
    O2 = 'r_1992'
    #AMO = 'r_1654'
    #PHO = 'r_2005'


    env_conds = [  {GLC: (-10.0, 999999.0)},
                  # {GLC: (-10.0, 999999.0), O2: (-1, 100000.0)},
                  # {GLY: (-20.0, 999999.0), GLC: (-10.0, 999999.0), O2: (-1, 100000.0)},
                  # {GLC: (-10.0, 999999.0), GLY: (-20.0, 999999.0), PHO: (-1.0, 999999.0)},
                  # {GLC: (-10.0, 999999.0), PHO: (-1.0, 999999.0)},
                  # {XYL: (-12.0, 999999.0)},
                  # {XYL: (-12.0, 999999.0), O2: (-1, 100000.0)},
                  # {GLY: (-20.0, 999999.0), O2: (-1, 100000.0)},
                  # {GLY: (-20.0, 999999.0)}
                  ]

    main(model_f, biomass_id=BIOMASS_ID, product_id=PRODUCT_ID, env_conditions=env_conds)
