""" Quantum Inspire SDK

Copyright 2018 QuTech Delft

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import unittest
from unittest import mock

from coreapi.auth import BasicAuthentication, TokenAuthentication
from qiskit.providers import QiskitBackendNotFoundError

from quantuminspire.exceptions import ApiError
from quantuminspire.qiskit.quantum_inspire_provider import QuantumInspireProvider, QI_URL


class TestQuantumInspireProvider(unittest.TestCase):
    simulator_backend_type = {'is_hardware_backend': False,
                              'name': 'qi_simulator',
                              'is_allowed': True,
                              'allowed_operations': {},
                              'max_number_of_shots': 4096,
                              'max_number_of_simultaneous_jobs': 3,
                              'topology': {'edges': []},
                              'number_of_qubits': 30}
    hardware_backend_type = {'is_hardware_backend': True,
                             'name': 'qi_hardware',
                             'is_allowed': True,
                             'allowed_operations': {
                                 'measure': ['measure_z', 'measure_x'],
                                 'measure_all': ['measure_all'],
                                 'parameterized_single_gates': ['rx', 'rz'],
                                 'single_gates': ['x', 's', 'z', 'h', 'tdag'],
                                 'dual_gates': ['cz'],
                             },
                             'max_number_of_shots': 2048,
                             'max_number_of_simultaneous_jobs': 1,
                             'topology': {'edges': [[2], [2], [0, 1, 3, 4], [2], [2]]},
                             'number_of_qubits': 5}

    hardware_backend_type2 = {'is_hardware_backend': True,
                              'name': 'qi_hardware',
                              'is_allowed': True,
                              'allowed_operations': {
                                  'measure': ['measure_z', 'measure_x'],
                                  'measure_all': ['measure_all'],
                                  'parameterized_single_gates': ['rx', 'ry', 'rz'],
                                  'single_gates': ['x', 'y', 'z', 'h', 'i', 't', 'tdag', 's', 'sdag'],
                                  'dual_gates': ['cz', 'cr', 'cnot', 'swap'],
                                  'triple_gates': ['toffoli'],
                              },
                              'max_number_of_shots': 4096,
                              'max_number_of_simultaneous_jobs': 1,
                              'topology': {'edges': [[1], [0]]},
                              'number_of_qubits': 2}

    def test_backends(self):
        with mock.patch('quantuminspire.qiskit.quantum_inspire_provider.QuantumInspireAPI') as api:
            quantum_inpire_provider = QuantumInspireProvider()
            with self.assertRaises(ApiError):
                quantum_inpire_provider.backends(name='quantum-inspire')
            email = 'bla@bla.bla'
            secret = 'secret'
            quantum_inpire_provider.set_basic_authentication(email, secret)
            authentication = BasicAuthentication(email, secret)
            api.assert_called_with(QI_URL, authentication)
            quantum_inpire_provider._api.get_backend_types.return_value = [self.simulator_backend_type]
            backend = quantum_inpire_provider.get_backend(name='qi_simulator')
            self.assertEqual('qi_simulator', backend.name())
            with self.assertRaises(QiskitBackendNotFoundError) as error:
                quantum_inpire_provider.get_backend(name='not-quantum-inspire')
            self.assertEqual(('No backend matches the criteria',), error.exception.args)

    def test_simulator_backend(self):
        with mock.patch('quantuminspire.qiskit.quantum_inspire_provider.QuantumInspireAPI') as api:
            quantum_inpire_provider = QuantumInspireProvider()
            with self.assertRaises(ApiError):
                quantum_inpire_provider.backends(name='quantum-inspire')
            email = 'bla@bla.bla'
            secret = 'secret'
            quantum_inpire_provider.set_basic_authentication(email, secret)
            authentication = BasicAuthentication(email, secret)
            api.assert_called_with(QI_URL, authentication)
            quantum_inpire_provider._api.get_backend_types.return_value = [self.simulator_backend_type]
            backend = quantum_inpire_provider.get_backend(name='qi_simulator')
            self.assertEqual('qi_simulator', backend.name())
            self.assertIsNone(backend.configuration().coupling_map)
            self.assertTrue(backend.configuration().simulator)
            self.assertEqual(30, backend.configuration().n_qubits)
            self.assertTrue(backend.configuration().memory)
            self.assertEqual(4096, backend.configuration().max_shots)
            self.assertEqual(3, backend.configuration().max_experiments)
            self.assertTrue(backend.configuration().conditional)
            self.assertEqual(backend.configuration().basis_gates, ['x', 'y', 'z', 'h', 'rx', 'ry', 'rz', 's', 'sdg',
                                                                   't', 'tdg', 'cx', 'ccx', 'u1', 'u2', 'u3', 'id',
                                                                   'swap', 'cz', 'snapshot'])

    def test_hardware_backend(self):
        with mock.patch('quantuminspire.qiskit.quantum_inspire_provider.QuantumInspireAPI') as api:
            quantum_inpire_provider = QuantumInspireProvider()
            with self.assertRaises(ApiError):
                quantum_inpire_provider.backends(name='quantum-inspire')
            email = 'bla@bla.bla'
            secret = 'secret'
            quantum_inpire_provider.set_basic_authentication(email, secret)
            authentication = BasicAuthentication(email, secret)
            api.assert_called_with(QI_URL, authentication)
            quantum_inpire_provider._api.get_backend_types.return_value = [self.hardware_backend_type]
            backend = quantum_inpire_provider.get_backend(name='qi_hardware')
            self.assertEqual('qi_hardware', backend.name())
            self.assertEqual(backend.configuration().coupling_map, [(0, 2), (1, 2), (2, 0), (2, 1),
                                                                    (2, 3), (2, 4), (3, 2), (4, 2)])
            self.assertFalse(backend.configuration().simulator)
            self.assertEqual(5, backend.configuration().n_qubits)
            self.assertTrue(backend.configuration().memory)
            self.assertEqual(2048, backend.configuration().max_shots)
            self.assertEqual(1, backend.configuration().max_experiments)
            self.assertFalse(backend.configuration().conditional)
            self.assertEqual(backend.configuration().basis_gates, ['rx', 'rz', 'x', 's', 'z', 'h', 'tdg', 'cz'])

    def test_hardware_backend2(self):
        with mock.patch('quantuminspire.qiskit.quantum_inspire_provider.QuantumInspireAPI') as api:
            quantum_inpire_provider = QuantumInspireProvider()
            with self.assertRaises(ApiError):
                quantum_inpire_provider.backends(name='quantum-inspire')
            email = 'bla@bla.bla'
            secret = 'secret'
            quantum_inpire_provider.set_basic_authentication(email, secret)
            authentication = BasicAuthentication(email, secret)
            api.assert_called_with(QI_URL, authentication)
            quantum_inpire_provider._api.get_backend_types.return_value = [self.hardware_backend_type2]
            backend = quantum_inpire_provider.get_backend(name='qi_hardware')
            self.assertEqual('qi_hardware', backend.name())
            self.assertEqual(backend.configuration().coupling_map, [(0, 1), (1, 0)])
            self.assertFalse(backend.configuration().simulator)
            self.assertEqual(2, backend.configuration().n_qubits)
            self.assertTrue(backend.configuration().memory)
            self.assertEqual(4096, backend.configuration().max_shots)
            self.assertEqual(1, backend.configuration().max_experiments)
            self.assertFalse(backend.configuration().conditional)
            self.assertEqual(backend.configuration().basis_gates, ['rx', 'ry', 'rz', 'x', 'y', 'z', 'h', 'id', 't',
                                                                   'tdg', 's', 'sdg', 'cz', 'cx', 'swap', 'ccx',
                                                                   'u1', 'u2', 'u3'])

    def test_set_authentication_details(self):
        with mock.patch('quantuminspire.qiskit.quantum_inspire_provider.QuantumInspireAPI') as api:
            quantum_inpire_provider = QuantumInspireProvider()
            with self.assertRaises(ApiError):
                quantum_inpire_provider.backends(name='quantum-inspire')
            email = 'bla@bla.bla'
            secret = 'secret'
            quantum_inpire_provider.set_authentication_details(email, secret)
            authentication = BasicAuthentication(email, secret)
            api.assert_called_with(QI_URL, authentication)
            quantum_inpire_provider._api.get_backend_types.return_value = [self.simulator_backend_type]
            backend = quantum_inpire_provider.get_backend(name='qi_simulator')
            self.assertEqual('qi_simulator', backend.name())

    def test_set_basic_authentication(self):
        with mock.patch('quantuminspire.qiskit.quantum_inspire_provider.QuantumInspireAPI') as api:
            quantum_inpire_provider = QuantumInspireProvider()
            with self.assertRaises(ApiError):
                quantum_inpire_provider.backends(name='quantum-inspire')
            email = 'bla@bla.bla'
            secret = 'secret'
            quantum_inpire_provider.set_basic_authentication(email, secret)
            authentication = BasicAuthentication(email, secret)
            api.assert_called_with(QI_URL, authentication)
            quantum_inpire_provider._api.get_backend_types.return_value = [self.simulator_backend_type]
            backend = quantum_inpire_provider.get_backend(name='qi_simulator')
            self.assertEqual('qi_simulator', backend.name())

    def test_set_basic_authentication_with_url(self):
        with mock.patch('quantuminspire.qiskit.quantum_inspire_provider.QuantumInspireAPI') as api:
            api.get_backend_types.return_value = [self.simulator_backend_type]
            quantum_inpire_provider = QuantumInspireProvider()
            with self.assertRaises(ApiError):
                quantum_inpire_provider.backends(name='quantum-inspire')
            email = 'bla@bla.bla'
            secret = 'secret'
            url = 'https/some-api.api'
            quantum_inpire_provider.set_basic_authentication(email, secret, url)
            authentication = BasicAuthentication(email, secret)
            api.assert_called_with(url, authentication)

    def test_set_token_authentication(self):
        with mock.patch('quantuminspire.qiskit.quantum_inspire_provider.QuantumInspireAPI') as api:
            quantum_inpire_provider = QuantumInspireProvider()
            with self.assertRaises(ApiError):
                quantum_inpire_provider.backends(name='quantum-inspire')
            token = 'This_is_a_nice_looking_token'
            quantum_inpire_provider.set_token_authentication(token)
            api.assert_called_once()

    def test_set_authentication(self):
        with mock.patch('quantuminspire.qiskit.quantum_inspire_provider.QuantumInspireAPI') as api:
            quantum_inpire_provider = QuantumInspireProvider()
            with self.assertRaises(ApiError):
                quantum_inpire_provider.backends(name='quantum-inspire')
            token = 'This_is_a_nice_looking_token'
            authentication = TokenAuthentication(token, scheme="token")
            quantum_inpire_provider.set_authentication(authentication)
            api.assert_called_with(QI_URL, authentication)
            authentication = BasicAuthentication('email', 'password')
            quantum_inpire_provider.set_authentication(authentication)
            api.assert_called_with(QI_URL, authentication)

    def test_string_method(self):
        quantum_inpire_provider = QuantumInspireProvider()
        expected = 'QI'
        actual = str(quantum_inpire_provider)
        self.assertEqual(expected, actual)
