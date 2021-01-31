from datetime import datetime
from recbole.trainer import HyperTuning
from recbole.quick_start import objective_function

hp = HyperTuning(
    objective_function=objective_function, algo='exhaustive',
    params_file='models\\pointwise\\mkr.test', fixed_config_file_list=['models\\pointwise\\mkr.yaml']
)

# run
hp.run()
# export result to the file
hp.export_result(output_file=f'models\\results\\mkr-{datetime.now():%Y%m%d%H%M%S%z}.result')
# print best parameters
print('best params: ', hp.best_params)
# print best result
print('best result: ')
print(hp.params2result[hp.params2str(hp.best_params)])
