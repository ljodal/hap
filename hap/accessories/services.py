from uuid import UUID

from .base import ServiceType
from .characteristics import (
    AccessoryFlags,
    Active,
    AdministratorOnlyAccess,
    AirQuality,
    AudioFeedback,
    BatteryLevel,
    Brightness,
    CarbonDioxideDetected,
    CarbonDioxideLevel,
    CarbonDioxidePeakLevel,
    CarbonMonoxideDetected,
    CarbonMonoxideLevel,
    CarbonMonoxidePeakLevel,
    ChargingState,
    ContactSensorState,
    CoolingThresholdTemperature,
    CurrentAirPurifierState,
    CurrentAmbientLightLevel,
    CurrentDoorState,
    CurrentFanState,
    CurrentHeaterCoolerState,
    CurrentHeatingCoolingState,
    CurrentHorizontalTiltAngle,
    CurrentHumidifierDehumidifierState,
    CurrentPosition,
    CurrentRelativeHumidity,
    CurrentSlatState,
    CurrentTemperature,
    CurrentTiltAngle,
    CurrentVerticalTiltAngle,
    FilterChangeIndication,
    FilterLifeLevel,
    FirmwareRevision,
    HardwareRevision,
    HeatingThresholdTemperature,
    HoldPosition,
    Hue,
    Identify,
    InUse,
    IsConfigured,
    LeakDetected,
    LockControlPoint,
    LockCurrentState,
    LockLastKnownAction,
    LockManagementAutoSecurityTimeout,
    LockPhysicalControls,
    LockTargetState,
    Logs,
    Manufacturer,
    Model,
    MotionDetected,
    Mute,
    Name,
    NitrogenDioxideDensity,
    ObstructionDetected,
    OccupancyDetected,
    On,
    OutletInUse,
    OzoneDensity,
    Pm2_5Density,
    Pm10Density,
    PositionState,
    ProgrammableSwitchEvent,
    ProgramMode,
    RelativeHumidityDehumidifierThreshold,
    RelativeHumidityHumidifierThreshold,
    RemainingDuration,
    ResetFilterIndication,
    RotationDirection,
    RotationSpeed,
    Saturation,
    SecuritySystemAlarmType,
    SecuritySystemCurrentState,
    SecuritySystemTargetState,
    SelectedRtpStreamConfiguration,
    SerialNumber,
    ServiceLabelIndex,
    ServiceLabelNamespace,
    SetDuration,
    SetupEndpoints,
    SlatType,
    SmokeDetected,
    StatusActive,
    StatusFault,
    StatusLowBattery,
    StatusTampered,
    StreamingStatus,
    SulphurDioxideDensity,
    SupportedAudioStreamConfiguration,
    SupportedRtpConfiguration,
    SupportedVideoStreamConfiguration,
    SwingMode,
    TargetAirPurifierState,
    TargetDoorState,
    TargetFanState,
    TargetHeaterCoolerState,
    TargetHeatingCoolingState,
    TargetHorizontalTiltAngle,
    TargetHumidifierDehumidifierState,
    TargetPosition,
    TargetRelativeHumidity,
    TargetTemperature,
    TargetTiltAngle,
    TargetVerticalTiltAngle,
    TemperatureDisplayUnits,
    ValveType,
    Version,
    VocDensity,
    Volume,
    WaterLevel,
)

AccessoryInformation = ServiceType(
    UUID("0000003E-0000-1000-8000-0026BB765291"),
    name="Accessory Information",
    required_characteristics=(
        Identify,
        Manufacturer,
        Model,
        Name,
        SerialNumber,
        FirmwareRevision,
    ),
    optional_characteristics=(HardwareRevision, AccessoryFlags),
)
AirPurifier = ServiceType(
    UUID("000000BB-0000-1000-8000-0026BB765291"),
    name="Air Purifier",
    required_characteristics=(Active, CurrentAirPurifierState, TargetAirPurifierState),
    optional_characteristics=(LockPhysicalControls, Name, SwingMode, RotationSpeed),
)
AirQualitySensor = ServiceType(
    UUID("0000008D-0000-1000-8000-0026BB765291"),
    name="Air Quality Sensor",
    required_characteristics=(AirQuality,),
    optional_characteristics=(
        StatusActive,
        StatusFault,
        StatusTampered,
        StatusLowBattery,
        Name,
        OzoneDensity,
        NitrogenDioxideDensity,
        SulphurDioxideDensity,
        Pm2_5Density,
        Pm10Density,
        VocDensity,
        CarbonMonoxideLevel,
        CarbonDioxideLevel,
    ),
)
BatteryService = ServiceType(
    UUID("00000096-0000-1000-8000-0026BB765291"),
    name="Battery Service",
    required_characteristics=(BatteryLevel, ChargingState, StatusLowBattery),
    optional_characteristics=(Name,),
)
CameraRtpStreamManagement = ServiceType(
    UUID("00000110-0000-1000-8000-0026BB765291"),
    name="Camera RTP Stream Management",
    required_characteristics=(
        SupportedVideoStreamConfiguration,
        SupportedAudioStreamConfiguration,
        SupportedRtpConfiguration,
        SelectedRtpStreamConfiguration,
        StreamingStatus,
        SetupEndpoints,
    ),
    optional_characteristics=(Name,),
)
CarbonDioxideSensor = ServiceType(
    UUID("00000097-0000-1000-8000-0026BB765291"),
    name="Carbon Dioxide Sensor",
    required_characteristics=(CarbonDioxideDetected,),
    optional_characteristics=(
        StatusActive,
        StatusFault,
        StatusLowBattery,
        StatusTampered,
        CarbonDioxideLevel,
        CarbonDioxidePeakLevel,
        Name,
    ),
)
CarbonMonoxideSensor = ServiceType(
    UUID("0000007F-0000-1000-8000-0026BB765291"),
    name="Carbon Monoxide Sensor",
    required_characteristics=(CarbonMonoxideDetected,),
    optional_characteristics=(
        StatusActive,
        StatusFault,
        StatusLowBattery,
        StatusTampered,
        CarbonMonoxideLevel,
        CarbonMonoxidePeakLevel,
        Name,
    ),
)
ContactSensor = ServiceType(
    UUID("00000080-0000-1000-8000-0026BB765291"),
    name="Contact Sensor",
    required_characteristics=(ContactSensorState,),
    optional_characteristics=(
        StatusActive,
        StatusFault,
        StatusTampered,
        StatusLowBattery,
        Name,
    ),
)
Door = ServiceType(
    UUID("00000081-0000-1000-8000-0026BB765291"),
    name="Door",
    required_characteristics=(CurrentPosition, PositionState, TargetPosition),
    optional_characteristics=(HoldPosition, ObstructionDetected, Name),
)
Doorbell = ServiceType(
    UUID("00000121-0000-1000-8000-0026BB765291"),
    name="Doorbell",
    required_characteristics=(ProgrammableSwitchEvent,),
    optional_characteristics=(Brightness, Volume, Name),
)
Fan = ServiceType(
    UUID("00000040-0000-1000-8000-0026BB765291"),
    name="Fan",
    required_characteristics=(On,),
    optional_characteristics=(RotationDirection, RotationSpeed, Name),
)
FanV2 = ServiceType(
    UUID("000000B7-0000-1000-8000-0026BB765291"),
    name="Fan v2",
    required_characteristics=(Active,),
    optional_characteristics=(
        CurrentFanState,
        TargetFanState,
        LockPhysicalControls,
        Name,
        RotationDirection,
        RotationSpeed,
        SwingMode,
    ),
)
FilterMaintenance = ServiceType(
    UUID("000000BA-0000-1000-8000-0026BB765291"),
    name="Filter Maintenance",
    required_characteristics=(FilterChangeIndication,),
    optional_characteristics=(FilterLifeLevel, ResetFilterIndication, Name),
)
Faucet = ServiceType(
    UUID("000000D7-0000-1000-8000-0026BB765291"),
    name="Faucet",
    required_characteristics=(Active,),
    optional_characteristics=(Name, StatusFault),
)
GarageDoorOpener = ServiceType(
    UUID("00000041-0000-1000-8000-0026BB765291"),
    name="Garage Door Opener",
    required_characteristics=(CurrentDoorState, TargetDoorState, ObstructionDetected),
    optional_characteristics=(LockCurrentState, LockTargetState, Name),
)
HeaterCooler = ServiceType(
    UUID("000000BC-0000-1000-8000-0026BB765291"),
    name="Heater Cooler",
    required_characteristics=(
        Active,
        CurrentHeaterCoolerState,
        TargetHeaterCoolerState,
        CurrentTemperature,
    ),
    optional_characteristics=(
        LockPhysicalControls,
        Name,
        SwingMode,
        CoolingThresholdTemperature,
        HeatingThresholdTemperature,
        TemperatureDisplayUnits,
        RotationSpeed,
    ),
)
HumidifierDehumidifier = ServiceType(
    UUID("000000BD-0000-1000-8000-0026BB765291"),
    name="Humidifier Dehumidifier",
    required_characteristics=(
        CurrentRelativeHumidity,
        CurrentHumidifierDehumidifierState,
        TargetHumidifierDehumidifierState,
        Active,
    ),
    optional_characteristics=(
        LockPhysicalControls,
        Name,
        SwingMode,
        WaterLevel,
        RelativeHumidityDehumidifierThreshold,
        RelativeHumidityHumidifierThreshold,
        RotationSpeed,
    ),
)
HumiditySensor = ServiceType(
    UUID("00000082-0000-1000-8000-0026BB765291"),
    name="Humidity Sensor",
    required_characteristics=(CurrentRelativeHumidity,),
    optional_characteristics=(
        StatusActive,
        StatusFault,
        StatusTampered,
        StatusLowBattery,
        Name,
    ),
)
IrrigationSystem = ServiceType(
    UUID("000000CF-0000-1000-8000-0026BB765291"),
    name="Irrigation System",
    required_characteristics=(Active, ProgramMode, InUse),
    optional_characteristics=(Name, RemainingDuration, StatusFault),
)
LeakSensor = ServiceType(
    UUID("00000083-0000-1000-8000-0026BB765291"),
    name="Leak Sensor",
    required_characteristics=(LeakDetected,),
    optional_characteristics=(
        StatusActive,
        StatusFault,
        StatusTampered,
        StatusLowBattery,
        Name,
    ),
)
LightSensor = ServiceType(
    UUID("00000084-0000-1000-8000-0026BB765291"),
    name="Light Sensor",
    required_characteristics=(CurrentAmbientLightLevel,),
    optional_characteristics=(
        Name,
        StatusActive,
        StatusFault,
        StatusTampered,
        StatusLowBattery,
    ),
)
Lightbulb = ServiceType(
    UUID("00000043-0000-1000-8000-0026BB765291"),
    name="Lightbulb",
    required_characteristics=(On,),
    optional_characteristics=(Brightness, Hue, Saturation, Name),
)
LockManagement = ServiceType(
    UUID("00000044-0000-1000-8000-0026BB765291"),
    name="Lock Management",
    required_characteristics=(LockControlPoint, Version),
    optional_characteristics=(
        Logs,
        AudioFeedback,
        LockManagementAutoSecurityTimeout,
        AdministratorOnlyAccess,
        LockLastKnownAction,
        CurrentDoorState,
        MotionDetected,
        Name,
    ),
)
LockMechanism = ServiceType(
    UUID("00000045-0000-1000-8000-0026BB765291"),
    name="Lock Mechanism",
    required_characteristics=(LockCurrentState, LockTargetState),
    optional_characteristics=(Name,),
)
Microphone = ServiceType(
    UUID("00000112-0000-1000-8000-0026BB765291"),
    name="Microphone",
    required_characteristics=(Volume, Mute),
    optional_characteristics=(Name,),
)
MotionSensor = ServiceType(
    UUID("00000085-0000-1000-8000-0026BB765291"),
    name="Motion Sensor",
    required_characteristics=(MotionDetected,),
    optional_characteristics=(
        StatusActive,
        StatusFault,
        StatusTampered,
        StatusLowBattery,
        Name,
    ),
)
OccupancySensor = ServiceType(
    UUID("00000086-0000-1000-8000-0026BB765291"),
    name="Occupancy Sensor",
    required_characteristics=(OccupancyDetected,),
    optional_characteristics=(
        Name,
        StatusActive,
        StatusFault,
        StatusTampered,
        StatusLowBattery,
    ),
)
Outlet = ServiceType(
    UUID("00000047-0000-1000-8000-0026BB765291"),
    name="Outlet",
    required_characteristics=(On, OutletInUse),
    optional_characteristics=(Name,),
)
SecuritySystem = ServiceType(
    UUID("0000007E-0000-1000-8000-0026BB765291"),
    name="Security System",
    required_characteristics=(SecuritySystemCurrentState, SecuritySystemTargetState),
    optional_characteristics=(
        StatusFault,
        StatusTampered,
        SecuritySystemAlarmType,
        Name,
    ),
)
ServiceLabel = ServiceType(
    UUID("000000CC-0000-1000-8000-0026BB765291"),
    name="Service Label",
    required_characteristics=(ServiceLabelNamespace,),
    optional_characteristics=(Name,),
)
Slat = ServiceType(
    UUID("000000B9-0000-1000-8000-0026BB765291"),
    name="Slat",
    required_characteristics=(SlatType, CurrentSlatState),
    optional_characteristics=(Name, CurrentTiltAngle, TargetTiltAngle, SwingMode),
)
SmokeSensor = ServiceType(
    UUID("00000087-0000-1000-8000-0026BB765291"),
    name="Smoke Sensor",
    required_characteristics=(SmokeDetected,),
    optional_characteristics=(
        StatusActive,
        StatusFault,
        StatusTampered,
        StatusLowBattery,
        Name,
    ),
)
Speaker = ServiceType(
    UUID("00000113-0000-1000-8000-0026BB765291"),
    name="Speaker",
    required_characteristics=(Mute,),
    optional_characteristics=(Name, Volume),
)
StatelessProgrammableSwitch = ServiceType(
    UUID("00000089-0000-1000-8000-0026BB765291"),
    name="Stateless Programmable Switch",
    required_characteristics=(ProgrammableSwitchEvent,),
    optional_characteristics=(Name, ServiceLabelIndex),
)
Switch = ServiceType(
    UUID("00000049-0000-1000-8000-0026BB765291"),
    name="Switch",
    required_characteristics=(On,),
    optional_characteristics=(Name,),
)
TemperatureSensor = ServiceType(
    UUID("0000008A-0000-1000-8000-0026BB765291"),
    name="Temperature Sensor",
    required_characteristics=(CurrentTemperature,),
    optional_characteristics=(
        StatusActive,
        StatusFault,
        StatusLowBattery,
        StatusTampered,
        Name,
    ),
)
Thermostat = ServiceType(
    UUID("0000004A-0000-1000-8000-0026BB765291"),
    name="Thermostat",
    required_characteristics=(
        CurrentHeatingCoolingState,
        TargetHeatingCoolingState,
        CurrentTemperature,
        TargetTemperature,
        TemperatureDisplayUnits,
    ),
    optional_characteristics=(
        CurrentRelativeHumidity,
        TargetRelativeHumidity,
        CoolingThresholdTemperature,
        HeatingThresholdTemperature,
        Name,
    ),
)
Valve = ServiceType(
    UUID("000000D0-0000-1000-8000-0026BB765291"),
    name="Valve",
    required_characteristics=(Active, InUse, ValveType),
    optional_characteristics=(
        SetDuration,
        RemainingDuration,
        IsConfigured,
        ServiceLabelIndex,
        StatusFault,
        Name,
    ),
)
Window = ServiceType(
    UUID("0000008B-0000-1000-8000-0026BB765291"),
    name="Window",
    required_characteristics=(CurrentPosition, TargetPosition, PositionState),
    optional_characteristics=(HoldPosition, ObstructionDetected, Name),
)
WindowCovering = ServiceType(
    UUID("0000008C-0000-1000-8000-0026BB765291"),
    name="Window Covering",
    required_characteristics=(CurrentPosition, TargetPosition, PositionState),
    optional_characteristics=(
        HoldPosition,
        TargetHorizontalTiltAngle,
        TargetVerticalTiltAngle,
        CurrentHorizontalTiltAngle,
        CurrentVerticalTiltAngle,
        ObstructionDetected,
        Name,
    ),
)
