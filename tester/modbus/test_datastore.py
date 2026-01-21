# -*- coding: utf-8 -*-

import threading
from unittest import TestCase, main

from cvp.modbus.datastore import ModbusDataStore
from cvp.modbus.exceptions import ModbusInvalidAddressError


class TestModbusDataStoreCoils(TestCase):
    def setUp(self) -> None:
        self.store = ModbusDataStore(coils_size=100)

    def test_get_coils_default(self) -> None:
        coils = self.store.get_coils(0, 10)
        self.assertEqual(len(coils), 10)
        self.assertTrue(all(c is False for c in coils))

    def test_set_and_get_coils(self) -> None:
        values = [True, False, True, True, False]
        self.store.set_coils(0, values)
        result = self.store.get_coils(0, 5)
        self.assertEqual(result, values)

    def test_set_single_coil(self) -> None:
        self.store.set_coil(5, True)
        self.assertEqual(self.store.get_coils(5, 1), [True])

    def test_invalid_address_negative(self) -> None:
        with self.assertRaises(ModbusInvalidAddressError):
            self.store.get_coils(-1, 1)

    def test_invalid_address_overflow(self) -> None:
        with self.assertRaises(ModbusInvalidAddressError):
            self.store.get_coils(95, 10)

    def test_invalid_count_zero(self) -> None:
        with self.assertRaises(ModbusInvalidAddressError):
            self.store.get_coils(0, 0)


class TestModbusDataStoreDiscreteInputs(TestCase):
    def setUp(self) -> None:
        self.store = ModbusDataStore(discrete_inputs_size=100)

    def test_get_discrete_inputs_default(self) -> None:
        inputs = self.store.get_discrete_inputs(0, 10)
        self.assertEqual(len(inputs), 10)
        self.assertTrue(all(i is False for i in inputs))

    def test_set_and_get_discrete_inputs(self) -> None:
        values = [True, True, False, True]
        self.store.set_discrete_inputs(10, values)
        result = self.store.get_discrete_inputs(10, 4)
        self.assertEqual(result, values)


class TestModbusDataStoreHoldingRegisters(TestCase):
    def setUp(self) -> None:
        self.store = ModbusDataStore(holding_registers_size=100)

    def test_get_holding_registers_default(self) -> None:
        registers = self.store.get_holding_registers(0, 10)
        self.assertEqual(len(registers), 10)
        self.assertTrue(all(r == 0 for r in registers))

    def test_set_and_get_holding_registers(self) -> None:
        values = [100, 200, 300, 400, 500]
        self.store.set_holding_registers(0, values)
        result = self.store.get_holding_registers(0, 5)
        self.assertEqual(result, values)

    def test_set_single_holding_register(self) -> None:
        self.store.set_holding_register(5, 12345)
        result = self.store.get_holding_registers(5, 1)
        self.assertEqual(result, [12345])

    def test_value_overflow_masking(self) -> None:
        self.store.set_holding_register(0, 0x10000)  # Exceeds 16-bit
        result = self.store.get_holding_registers(0, 1)
        self.assertEqual(result, [0])  # Should be masked to 0

    def test_invalid_address(self) -> None:
        with self.assertRaises(ModbusInvalidAddressError):
            self.store.get_holding_registers(95, 10)


class TestModbusDataStoreInputRegisters(TestCase):
    def setUp(self) -> None:
        self.store = ModbusDataStore(input_registers_size=100)

    def test_get_input_registers_default(self) -> None:
        registers = self.store.get_input_registers(0, 10)
        self.assertEqual(len(registers), 10)
        self.assertTrue(all(r == 0 for r in registers))

    def test_set_and_get_input_registers(self) -> None:
        values = [1000, 2000, 3000]
        self.store.set_input_registers(0, values)
        result = self.store.get_input_registers(0, 3)
        self.assertEqual(result, values)


class TestModbusDataStoreThreadSafety(TestCase):
    def test_concurrent_read_write(self) -> None:
        store = ModbusDataStore()
        errors = []

        def writer() -> None:
            try:
                for i in range(100):
                    store.set_holding_registers(0, [i, i + 1, i + 2])
            except Exception as e:
                errors.append(e)

        def reader() -> None:
            try:
                for _ in range(100):
                    store.get_holding_registers(0, 3)
            except Exception as e:
                errors.append(e)

        threads = []
        for _ in range(5):
            threads.append(threading.Thread(target=writer))
            threads.append(threading.Thread(target=reader))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0)


class TestModbusDataStoreReset(TestCase):
    def test_reset(self) -> None:
        store = ModbusDataStore(
            coils_size=10,
            discrete_inputs_size=10,
            holding_registers_size=10,
            input_registers_size=10,
        )

        store.set_coils(0, [True, True, True])
        store.set_holding_registers(0, [100, 200, 300])

        store.reset()

        self.assertEqual(store.get_coils(0, 3), [False, False, False])
        self.assertEqual(store.get_holding_registers(0, 3), [0, 0, 0])


class TestModbusDataStoreProperties(TestCase):
    def test_size_properties(self) -> None:
        store = ModbusDataStore(
            coils_size=100,
            discrete_inputs_size=200,
            holding_registers_size=300,
            input_registers_size=400,
        )
        self.assertEqual(store.coils_size, 100)
        self.assertEqual(store.discrete_inputs_size, 200)
        self.assertEqual(store.holding_registers_size, 300)
        self.assertEqual(store.input_registers_size, 400)


if __name__ == "__main__":
    main()
