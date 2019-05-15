from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop


with open('requirements.txt', 'r') as f:
    install_requires = list()
    dependency_links = list()
    for line in f:
        re = line.strip()
        if re:
            install_requires.append(re)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # This is used so that it will pass d3m metadata submission process. The dsbox-featurizer package depends on
        import subprocess
        result = subprocess.check_output(['pip', 'list'])
        lines = str(result).split('\\n')
        for line in lines[2:]:
            part = line.split()
            if 'dsbox-featurizer' in part[0]:
                print(line)
                if '0' == part[1].split('.')[0]:
                    subprocess.call(['pip', 'uninstall', '-y', 'dsbox-featurizer'])
        import keras.applications.resnet50 as resnet50
        import keras.applications.vgg16 as vgg16
        resnet50.ResNet50(weights='imagenet')
        vgg16.VGG16(weights='imagenet', include_top=False)
        install.run(self)

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        import keras.applications.resnet50 as resnet50
        import keras.applications.vgg16 as vgg16
        resnet50.ResNet50(weights='imagenet')
        vgg16.VGG16(weights='imagenet', include_top=False)
        develop.run(self)

setup(name='dsbox-primitives',
      version='1.0.0',
      description='DSBox data processing primitives for both cleaning and featurizer',
      author='USC ISI',
      url='https://github.com/usc-isi-i2/dsbox-primitives.git',
      maintainer_email='kyao@isi.edu',
      maintainer='Ke-Thia Yao',
      license='MIT',
      packages=[
                'dsbox',
                'dsbox.datapreprocessing',
                'dsbox.datapreprocessing.cleaner', 
                'dsbox.datapostprocessing',
                'dsbox.datapreprocessing.featurizer',
                'dsbox.datapreprocessing.featurizer.multiTable',
                'dsbox.datapreprocessing.featurizer.image',
                'dsbox.datapreprocessing.featurizer.pass',
                'dsbox.datapreprocessing.featurizer.timeseries'
               ],
      zip_safe=False,
      python_requires='>=3.6',
      install_requires=install_requires,
      keywords='d3m_primitive',
      entry_points={
          'd3m.primitives': [
              'data_cleaning.cleaning_featurizer.DSBOX = dsbox.datapreprocessing.cleaner:CleaningFeaturizer',
              'data_preprocessing.encoder.DSBOX = dsbox.datapreprocessing.cleaner:Encoder',
              'data_preprocessing.unary_encoder.DSBOX = dsbox.datapreprocessing.cleaner:UnaryEncoder',
              'data_preprocessing.greedy_imputation.DSBOX = dsbox.datapreprocessing.cleaner:GreedyImputation',
              'data_preprocessing.iterative_regression_imputation.DSBOX = dsbox.datapreprocessing.cleaner:IterativeRegressionImputation',
              'data_preprocessing.mean_imputation.DSBOX = dsbox.datapreprocessing.cleaner:MeanImputation',
              'normalization.iqr_scaler.DSBOX = dsbox.datapreprocessing.cleaner:IQRScaler',
              'data_cleaning.labeler.DSBOX = dsbox.datapreprocessing.cleaner:Labler',
              'normalization.denormalize.DSBOX = dsbox.datapreprocessing.cleaner:Denormalize',
              'schema_discovery.profiler.DSBOX = dsbox.datapreprocessing.cleaner:Profiler',
              'data_cleaning.column_fold.DSBOX = dsbox.datapreprocessing.cleaner:FoldColumns',
              'data_preprocessing.vertical_concatenate.DSBOX = dsbox.datapostprocessing:VerticalConcat',
              'data_preprocessing.ensemble_voting.DSBOX = dsbox.datapostprocessing:EnsembleVoting',
              'data_preprocessing.unfold.DSBOX = dsbox.datapostprocessing:Unfold',
              'data_preprocessing.splitter.DSBOX = dsbox.datapreprocessing.cleaner:Splitter',
              'data_preprocessing.horizontal_concat.DSBOX = dsbox.datapostprocessing:HorizontalConcat',
              'data_transformation.to_numeric.DSBOX = dsbox.datapreprocessing.cleaner:ToNumeric',
              'data_preprocessing.do_nothing.DSBOX = dsbox.datapreprocessing.featurizer.pass:DoNothing',
              'data_preprocessing.do_nothing_for_dataset.DSBOX = dsbox.datapreprocessing.featurizer.pass:DoNothingForDataset',
              'feature_extraction.multitable_featurization.DSBOX = dsbox.datapreprocessing.featurizer.multiTable:MultiTableFeaturization',
              'data_preprocessing.dataframe_to_tensor.DSBOX = dsbox.datapreprocessing.featurizer.image:DataFrameToTensor',
              'feature_extraction.yolo.DSBOX = dsbox.datapreprocessing.featurizer.image:Yolo',
              'feature_extraction.lstm.DSBOX = dsbox.datapreprocessing.featurizer.image:LSTM',
              'feature_extraction.vgg16_image_feature.DSBOX = dsbox.datapreprocessing.featurizer.image:Vgg16ImageFeature',
              'feature_extraction.inceptionV3_image_feature.DSBOX = dsbox.datapreprocessing.featurizer.image:InceptionV3ImageFeature',
              'feature_extraction.resnet50_image_feature.DSBOX = dsbox.datapreprocessing.featurizer.image:ResNet50ImageFeature',
              'data_preprocessing.time_series_to_list.DSBOX = dsbox.datapreprocessing.featurizer.timeseries:TimeseriesToList',
              'feature_extraction.random_projection_timeseries_featurization.DSBOX = dsbox.datapreprocessing.featurizer.timeseries:RandomProjectionTimeSeriesFeaturization',
              'data_transformation.group_up_by_timeseries.DSBOX = dsbox.datapreprocessing.featurizer.timeseries:GroupUpByTimeSeries',
              'time_series_forecasting.arima.DSBOX = dsbox.datapreprocessing.featurizer.timeseries:AutoArima',
              'time_series_forecasting.rnn_time_series.DSBOX = dsbox.datapreprocessing.featurizer.timeseries:RNNTimeSeries',
              'data_augmentation.wikifier.DSBOX = dsbox.datapreprocessing.cleaner:Wikifier',
              'data_augmentation.datamart_download.DSBOX = dsbox.datapreprocessing.cleaner:DatamartDownload',
              'data_augmentation.datamart_augmentation.DSBOX = dsbox.datapreprocessing.cleaner:DatamartAugmentation',
          ],
      },
      cmdclass={
          'develop': PostDevelopCommand,
          'install': PostInstallCommand
      })
