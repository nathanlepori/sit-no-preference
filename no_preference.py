import no_preference.processing.ner_training.training_ui as training_ui
from no_preference.util import create_data_dir

if __name__ == '__main__':
    create_data_dir()
    training_ui.run()
