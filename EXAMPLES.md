# Examples and Usage

## Basic Usage

Once configured, the integration automatically creates sensors that you can use in your Home Assistant dashboard and automations.

## Available Sensors

The integration provides the following sensors:

- `sensor.apsystems_current_power` - Real-time power generation in Watts
- `sensor.apsystems_today_energy` - Energy generated today in kWh
- `sensor.apsystems_lifetime_energy` - Total energy generated in kWh
- `sensor.apsystems_max_power` - Maximum power capacity in Watts

## Dashboard Examples

### Simple Entities Card

```yaml
type: entities
title: Solar Power
entities:
  - entity: sensor.apsystems_current_power
    name: Current Power
  - entity: sensor.apsystems_today_energy
    name: Today's Energy
  - entity: sensor.apsystems_lifetime_energy
    name: Total Energy
```

### Gauge Card for Current Power

```yaml
type: gauge
entity: sensor.apsystems_current_power
name: Solar Power
unit: W
min: 0
max: 5000
needle: true
```

### Energy Dashboard Integration

The sensors automatically integrate with Home Assistant's Energy Dashboard:

1. Go to **Settings** → **Dashboards** → **Energy**
2. Add **Solar Panels**
3. Select `sensor.apsystems_today_energy`
4. Configure and save

## Automation Examples

### Notify When Power Exceeds Threshold

```yaml
automation:
  - alias: High Solar Power Notification
    trigger:
      - platform: numeric_state
        entity_id: sensor.apsystems_current_power
        above: 3000
    action:
      - service: notify.mobile_app
        data:
          message: "Solar panels generating {{ states('sensor.apsystems_current_power') }}W!"
```

### Track Daily Energy Production

```yaml
automation:
  - alias: Daily Solar Report
    trigger:
      - platform: time
        at: "20:00:00"
    action:
      - service: notify.mobile_app
        data:
          message: >
            Today's solar energy: {{ states('sensor.apsystems_today_energy') }} kWh
```

### Monitor System Status

```yaml
automation:
  - alias: Solar System Offline Alert
    trigger:
      - platform: state
        entity_id: sensor.apsystems_current_power
        to: "unavailable"
        for:
          minutes: 30
    action:
      - service: notify.mobile_app
        data:
          message: "Solar system appears to be offline"
          title: "Solar System Alert"
```

## Lovelace UI Examples

### Power Flow Card

You can use the integration with the popular power flow card:

```yaml
type: custom:power-flow-card
entities:
  solar: sensor.apsystems_current_power
```

### Statistics Card

```yaml
type: statistics-graph
entities:
  - sensor.apsystems_today_energy
stat_types:
  - sum
period: day
```

## Using with Node-RED

Example Node-RED flow to process solar data:

1. Use the `current-state` node to get sensor values
2. Process with function nodes
3. Store in database or send notifications

## Template Sensors

Create custom template sensors for additional calculations:

```yaml
template:
  - sensor:
      - name: "Solar Efficiency"
        unit_of_measurement: "%"
        state: >
          {% set current = states('sensor.apsystems_current_power')|float %}
          {% set max_power = states('sensor.apsystems_max_power')|float %}
          {% if max_power > 0 %}
            {{ ((current / max_power) * 100)|round(1) }}
          {% else %}
            0
          {% endif %}
```

## Tips and Tricks

1. **Energy Dashboard**: Add the integration to track solar production over time
2. **History Stats**: Use history stats sensor to calculate total production hours
3. **Utility Meter**: Create daily, monthly, and yearly energy totals
4. **Grafana**: Export sensor data to Grafana for advanced visualization

## Advanced Configuration

### Custom Update Interval

The default update interval is 5 minutes. To change this, you would need to modify the `UPDATE_INTERVAL` constant in the integration files (requires manual code modification).

### Multiple Systems

To monitor multiple APSystems inverters, simply add the integration multiple times with different System IDs.
