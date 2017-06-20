'''Test base class'''
from unittest import TestCase
from unittest.mock import patch
from abc import abstractmethod
from os.path import abspath, dirname, join

import numpy as np

from seq2vec.util import DataGenterator

class TestSeq2vecBaseClass(object):

    def setUp(
            self,
            latent_size=100,
            encoding_size=100,
            max_length=5,
            model_path='seq2vec_model.h5'
    ):
        self.latent_size = latent_size
        self.encoding_size = encoding_size
        self.max_length = max_length

        self.dir_path = dirname(abspath(__file__))
        self.model_path = join(self.dir_path, model_path)
        self.data_path = join(self.dir_path, 'test_corpus.txt')

        self.model = self.initialize_model()
        self.input_transformer = self.initialize_input_transformer()
        self.output_transformer = self.initialize_output_transformer()

        self.data_generator = DataGenterator(
            self.data_path,
            self.input_transformer,
            self.output_transformer,
            batch_size=10
        )

        self.train_seq = [
            ['我', '有', '一個', '蘋果'],
            ['我', '有', '一支', '筆'],
            ['我', '有', '一個', '鳳梨'],
        ]
        self.test_seq = [
            ['我', '愛', '吃', '鳳梨'],
        ]

    @abstractmethod
    def initialize_model(self):
        pass

    @abstractmethod
    def initialize_input_transformer(self):
        pass

    @abstractmethod
    def initialize_output_transformer(self):
        pass

    @patch('keras.models.Model.fit')
    def test_fit(self, _):
        self.model.fit(self.train_seq)
        result = self.model.transform(self.test_seq)
        self.assertEqual(result.shape[1], self.encoding_size)

    @patch('keras.models.Model.fit_generator')
    def test_fit_generator(self, _):
        self.model.fit_generator(
            self.data_generator,
            self.data_generator,
            batch_number=2
        )

        result = self.model(self.train_seq)
        self.assertEqual(result.shape[1], self.encoding_size)
