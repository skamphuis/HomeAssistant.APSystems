# Quick Start Guide

Get your APSystems solar inverter connected to Home Assistant in minutes!

## Prerequisites

✅ Home Assistant installed and running  
✅ APSystems solar inverter with EMA monitoring  
✅ APSystems OpenAPI credentials (App ID, App Secret, System ID)  

> **Don't have API credentials yet?** Contact APSystems support or visit their developer portal to request OpenAPI access.

## Installation (Choose One Method)

### Method 1: HACS (Easiest)

1. Open **HACS** in Home Assistant
2. Go to **Integrations**
3. Click **⋮** (3 dots) → **Custom repositories**
4. Add: `https://github.com/skamphuis/HomeAssistant.APSystems`
5. Category: **Integration**
6. Search for **APSystems OpenAPI**
7. Click **Download**
8. **Restart Home Assistant**

### Method 2: Manual

1. Download the [latest release](https://github.com/skamphuis/HomeAssistant.APSystems/releases)
2. Extract the zip file
3. Copy `custom_components/apsystems_openapi` to your Home Assistant `custom_components` folder
4. **Restart Home Assistant**

## Configuration

### Step 1: Add Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration** 
3. Search for **APSystems OpenAPI**

### Step 2: Enter Credentials

Fill in your credentials:

- **App ID**: Your APSystems OpenAPI App ID
- **App Secret**: Your APSystems OpenAPI App Secret
- **System ID**: Your system ID (found in EMA portal)

Example:
```
App ID: abc123def456
App Secret: secretkey789xyz
System ID: SYS123456789
```

### Step 3: Done! 🎉

The integration will:
- ✅ Test your connection
- ✅ Create your solar system device
- ✅ Set up 4 sensors automatically
- ✅ Start updating data every 5 minutes

## Your Sensors

After setup, you'll have these sensors:

| Sensor | What It Shows | Unit |
|--------|---------------|------|
| **Current Power** | Live power generation | W |
| **Today Energy** | Energy generated today | kWh |
| **Lifetime Energy** | Total energy ever generated | kWh |
| **Max Power** | System's maximum capacity | W |

Entity IDs:
- `sensor.apsystems_current_power`
- `sensor.apsystems_today_energy`
- `sensor.apsystems_lifetime_energy`
- `sensor.apsystems_max_power`

## Quick Dashboard Setup

### Option 1: Simple Card

1. Edit your dashboard
2. Add **Entities Card**
3. Select your APSystems sensors
4. Save

### Option 2: Copy This YAML

Click **Edit Dashboard** → **Add Card** → **Manual** and paste:

```yaml
type: entities
title: Solar Power
entities:
  - entity: sensor.apsystems_current_power
    name: Current Power
    icon: mdi:solar-power
  - entity: sensor.apsystems_today_energy
    name: Today's Production
    icon: mdi:solar-power
  - entity: sensor.apsystems_lifetime_energy
    name: Total Production
    icon: mdi:counter
```

### Option 3: Gauge for Current Power

```yaml
type: gauge
entity: sensor.apsystems_current_power
name: Solar Power
min: 0
max: 5000
needle: true
```

## Add to Energy Dashboard

1. Go to **Settings** → **Dashboards** → **Energy**
2. Click **Add Solar Production**
3. Select `sensor.apsystems_today_energy`
4. Click **Save**

Now you can track your solar production over time! 📊

## Create Your First Automation

Get notified when your panels are producing well:

1. Go to **Settings** → **Automations & Scenes**
2. Click **Create Automation**
3. Use this YAML:

```yaml
alias: High Solar Production Alert
trigger:
  - platform: numeric_state
    entity_id: sensor.apsystems_current_power
    above: 3000
action:
  - service: notify.mobile_app_your_phone
    data:
      message: "☀️ Solar panels generating {{ states('sensor.apsystems_current_power') }}W!"
      title: "High Solar Production"
```

## Troubleshooting

### ❌ "Cannot Connect" Error
- Check your internet connection
- Verify App ID and App Secret are correct
- Make sure your system is online in EMA portal

### ❌ "Invalid Authentication" Error
- Double-check credentials (no extra spaces)
- Ensure API access is active
- Try generating new credentials from APSystems

### ⚠️ Sensors Show "Unavailable"
- Wait 5-10 minutes for first data update
- Check **Settings** → **System** → **Logs** for errors
- Verify your system is online and reporting to EMA

### 💡 Need More Help?
- Check the [full installation guide](INSTALLATION.md)
- Review [examples and usage](EXAMPLES.md)
- [Open an issue](https://github.com/skamphuis/HomeAssistant.APSystems/issues) on GitHub

## What's Next?

Now that you're set up, explore more:

- 📊 **[View Usage Examples](EXAMPLES.md)** - Dashboard cards, automations, templates
- 🔧 **[API Documentation](API.md)** - Technical details for developers
- 🤝 **[Contributing Guide](CONTRIBUTING.md)** - Help improve the integration

## Getting API Credentials

If you don't have APSystems OpenAPI credentials yet:

1. **Contact APSystems Support**
   - Email: support@APSystems.com
   - Phone: Check APSystems website for your region

2. **Request OpenAPI Access**
   - Mention you need "End User OpenAPI access"
   - Provide your system ID from EMA portal

3. **Receive Credentials**
   - You'll get an App ID and App Secret
   - Use these to configure the integration

4. **Find Your System ID**
   - Log into [APSystems EMA portal](https://ema.apsystemsema.com)
   - Your System ID is shown in your account dashboard

---

**Enjoying the integration?** ⭐ Star the [GitHub repository](https://github.com/skamphuis/HomeAssistant.APSystems) and share it with others!
