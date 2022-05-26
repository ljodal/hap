from hap.accessories import CurrentTemperature, TemperatureSensor


def test_current_temperature() -> None:
    char_spec = CurrentTemperature()
    assert char_spec.type is CurrentTemperature
    assert char_spec.initial_value is None
    assert char_spec.event_notifications_enabled is False


def test_current_temperature_initial_value() -> None:
    char_spec = CurrentTemperature(initial_value=20)  # type: ignore[arg-type]
    assert char_spec.type is CurrentTemperature
    assert char_spec.initial_value == 20
    assert char_spec.event_notifications_enabled is False


def test_current_temperature_event_notifications_enabled() -> None:
    char_spec = CurrentTemperature(event_notifications_enabled=True)
    assert char_spec.type is CurrentTemperature
    assert char_spec.initial_value is None
    assert char_spec.event_notifications_enabled is True


def test_temperature_sensor() -> None:

    service_spec = TemperatureSensor(CurrentTemperature())
    assert service_spec.type is TemperatureSensor
    assert service_spec.primary is False
    assert service_spec.hidden is False
    assert len(service_spec.characteristics) == 1

    char_spec = service_spec.characteristics[0]
    assert char_spec.type is CurrentTemperature
