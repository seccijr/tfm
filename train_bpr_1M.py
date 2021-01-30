from logging import getLogger
from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from recbole.utils import init_logger, get_model, get_trainer, init_seed

model = 'BPR'
dataset = 'mind_1M'
config_dict = {
    'data_path': 'data',
    'epochs': 5,
    'load_col': {
        'inter': ['user_id', 'item_id', 'click', 'timestamp'],
        'kg': ['head_id', 'relation_id', 'tail_id'],
        'link': ['item_id', 'entity_id']
    },
    'training_neg_sample_num': 0,
    'threshold': {
        'click': 1
    },
    'eval_setting': 'RO_RS,'
}
saved = False

config = Config(model=model, dataset=dataset, config_file_list=[], config_dict=config_dict)
init_seed(config['seed'], config['reproducibility'])

# logger initialization
init_logger(config)
logger = getLogger()

logger.info(config)

# dataset filtering
dataset = create_dataset(config)
logger.info(dataset)

# dataset splitting
train_data, valid_data, test_data = data_preparation(config, dataset)

# model loading and initialization
model = get_model(config['model'])(config, train_data).to(config['device'])
logger.info(model)

# trainer loading and initialization
trainer = get_trainer(config['MODEL_TYPE'], config['model'])(config, model)

# model training
best_valid_score, best_valid_result = trainer.fit(
    train_data, valid_data, saved=saved, show_progress=config['show_progress']
)

# model evaluation
test_result = trainer.evaluate(test_data, load_best_model=saved, show_progress=config['show_progress'])

logger.info('best valid result: {}'.format(best_valid_result))
logger.info('test result: {}'.format(test_result))

# return {
#     'best_valid_score': best_valid_score,
#     'valid_score_bigger': config['valid_metric_bigger'],
#     'best_valid_result': best_valid_result,
#     'test_result': test_result
# }
