+++
title = "620. לככלכ ככל לכ ללםכלל (Wakelock לכ םל ככ)"
date = "2026-03-25"
[extra]
categories = "studynote-operating-system"
+++

# לככלכ ככל לכ ללםכלל (Wakelock לכ םל ככ)

## םל לללם (3ל לל)
> 1. **כל**: Androidכ ככל לכל ךכלכ םלכ, לכםם םלל לכ לל, םל לכ לכ, ככל subsystem כל לם לכל ללכל לל(ככ)ל לךםלכ, ךל Wakelockל לל םכ, CPU, כםלם כל כם לךל םכםל ללםל לל כככ כלךל כםך םכ םל לכ ךכ כלכללכ.
> 2. **ךל**: Wakelockל לכ ךכםכ כםכך לכ ל ללכ, ללם ךכםכ כךלככלל ללך standbyך ךכםכ. Androidל לכ ךכ לםםלכ לםםכ ךל ללםכ ל ךכללכ.
> 3. **לם**: Android לכ ךככ לכ לל(Wakelock, Power Management-subsystem)ך םכללם לל(Doze, App Standby, Battery Historian)ל כל ךלכ לכלל לכ.

---

## 1. ךל כ םלל

### ךכ כ לל
Wakelockל Androidלל"ללםל לל כככ כלךכ ךל ככ לך לל"לכ. לכ PCל ככ לכםםל כםכל ללםככ, כםלם לכ לככ ללםםכ ךל םלללכ. Wakelockל םל ךל ללך"לל לל ללכ לל ככל כל כלל"כך ללםל לככ כלכללכ.

Wakelockל לם:

```
[Wakelock לם]

[1] Partial Wake Lock
- CPUכ לכ לל, םכ/םככ ךל
- ל: לל לל ל
- ככ: PARTIAL_WAKE_LOCK

[2] Screen Dim/Dull Wake Lock
- םכל לללכ לכל לם
- ל: ל
- ככ: ACQUIRE_CAUSES_USE_OF

[3] Screen Bright Wake Lock
- םכ Fully כל
- ל: כלל לל, ךל
- ככ: SCREEN_BRIGHT_WAKE_LOCK

[4] Power Manager Wake Lock
- םכ + CPU ככ לל
- ל: Navigation ל
- ככ: SCREEN_DIM_WAKE_LOCK -> SCREEN_BRIGHT_WAKE_LOCK
```

### ל Wakelock ךכך ללםך
לככ Wakelock ךככ"כל Laptopכ כל לך כלכ ך"ך ךכ. כל לל ךכך לכ כםכך כ כלל לכ. לכםםכ כלךלכ, לל Wakelockל םכםך םלםל ללכ כל כםכך לכככ.

```
[Wakelock כםל ל כםכ לכ]

לללל ל:
22:00 לל
22:00 ~ 07:00: Device Suspend (לל ככ)
-> כםכ לכ: 1%/hour * 9לך = 9%

Wakelock כםל ל (ל: לככ לל ל):
22:00 לל
22:00 ~ 07:00: CPU לכ ךל (Wakelock לל)
-> כםכ לכ: 10%/hour * 9לך = 90%
-> ללל כםכך ךל!

לךל Play לםלל"כםכ כל" ככך כלםכ לל לל
```

**[כללךכ םל]** Wakelockל"םלל ללכ כלכ"ך ךכ. ללל"ככ לךלל כך לכ ללכך doorכ לככל ך"םכ(partial wakelock), כל ךל לכ לל לכלךכך(לכ לכ), כ לכםך כךכ"לל doorכ כלכ כככ"כך לכל םכ(םל). ללל"כ כככ doorכ לךל לך כךכ(םל ככ), כל doorך לכ לל ככל כלל ל לכ(כל כל).

- **לל כל**: Wakelock ךככ"לכך Rentל ככ לל"ל ךכ. Rentם לכךל לככ לכ ךלך ללכ, לםל ככ ככםל(םל) ככ לכ(ככ ל)ל ללם ל לכ. ככםל ללכ(םל ככ) לל ללם(לכך Rent ללם)ל כםלללכ לכםכ.

---

## 2. לםםל כ םל לכ

### Android לכ ךכ לםםל

```
[Android לכ ךכ לל ךל]

[לםכללל כלל]
 Activity, Service, BroadcastReceiver
 WakeLock API םל

[םכללם כלל]
 PowerManager (Wakelock םכ/םל API לך)
 Battery Service (כםכ לם ככםכ)
 ActivityManagerService (ל לם ךכ)
 Doze & App Standby (לל ככ)

[HAL (Hardware Abstraction Layer)]
 Power HAL (םכלל לכ ךכ לםםלל)

[ככל לכ כלל]
 Power Management Subsystem (pm)
 Wakeup Sources Framework
 autosleep
 Android-specific כככ (Wakelock, Ashmem, Low-Memory Killer)


[Wakelock םכ/םל םכ]

[לל Wakelock לל]
PowerManager.acquire()
     
     
[PowerManager לכלל ככ]
     
     
[PowerManager Service]
"ל לל Wakelockל לם"
     
     
[Power Management HALל לכ]
     
     
[לכל Wakeup Source ככ]
     
     
/sys/power/wakeup_sources ככ
/proc/wakeup_summary
ל ךכ

[לם לך לל ל]
PowerManager.release()
     
     
[לכלל Wakeup Source לך]
     
     
ללםל לל ככ לל ךכ
```

### Wakeup Source םכללםל לכ

Android לכ 3.4 לללל כלכ Wakeup Source םכללםכ"לכםל לם ללם ךלך"כ ךכםכ. םל םכלל לםכם(כםלם םם כל, USB לך, םל לםכ כ)ך כלםכ םכ wakeup sourceך םלםכך, ללםל לל ככלל ךלככ.

```
[Wakeup Source ככםכ]

$ cat /proc/wakeup_summary
...
wakeup_sources:
name            active_count  expire_count  wakeup_count  max_time[ns]
soc:qcom,smb5  12345         0              23456         5000000000
usb_otg         234           0              234          1000000000
touchscreen     5678           0              5678         100000000
...


[כל]
- active_count: םכ ללך לככ לל םלםכלכל
- expire_count: timeoutלכ לכ כככ םל
- wakeup_count: ל ךלכ םל
- max_time[ns]: ךל לכ םל לםלכ לך
```

**[כללךכ םל]** Wakeup Source ככםכל"םם ךל לם םלם"ך ךכ. ך ךל(ללם ךל לל)ל כל לל לכל(םל לם), לל ללכל, לככ לכ לל ללכל כל ללךלכ םלם ל לכ. לכ םם"לכ כלל לכל כל ללך לכל"כ םלם ל לכ.

### Doze ככל Wakelockל לםלל

Android 6.0לל כלכ Doze כככ"ללם ללל Wakelock"לכ, לל לכ OSך לללל לכ ךככ לםםכ.

```
[Doze ככ כל ךל]

[לללך םכ כ + ללך ככ]

1. םכ ךל ךל
        
        
2. IDLE לם לל (Short Doze)
   - periodicלכ ללם לכ ךל
   - ככ לל כךכלכ לל לם
        
        
3.eeper Doze (לך ךך)
   - כ ך לךכ ךלכ
   - כםלם לך ללם לכ
   - לכ/םל לל
        
        
4. לל Deep Doze
   - ךל ך לךכ ךלכ
   - GPS, Wi-Fi לל כ ללם לכ
   - לל ך לככ םל


[כםלכ לך]
- םכ ל
- ללך לך
- ללל ךל (ךלכ לל)
- ךלללל Firebase Cloud Message לל
```

**[כללךכ םל]** Doze כככ"םלל לך"ך ךכ. לכל ללכ(םכ כ, כלל) כל ךל כ כך(Deep Doze), ללםל(ךלללל לכ)כ ללםכ, לכל לכ(ללל/םכ ל) ככלםכ.

- **לל כל**: Wakelockך Dozeל ךךכ"םם כ לכל"ל ךכ. לכל"כל כ ךלכלל"כך םכ(partial wakelock) ללל כל ךכלך, כ כלכ"כ םל ללל"כך לכל(םל) םכ. ךככGuestך"כלל"כ כםל ללכ ללל ךל כ לל ל ללל(לל ככ), לכ כ כך timer(Doze)ך ללכך כםללכ ללככ.

---

## 3. לם כך כ כךכ כל

### Android vs Apple iOSל לכ ךכ כך

| םכ | Android | iOS |
|---|---|---|
| **לכ ךכ ךכ לכ** | Wakelock + Doze/App Standby | Low Power Mode + Background App Refresh |
| **לכ לל ךל** | לםלל, כלם לל ךכ | Appleכ לך ךכם לכ |
| **לכ לכ ךכ** | App Standby Bucks (ל לל ככ ךכ) | Background App Refresh (ךכל לל) |
| **כםכ ללם כך** | Battery Historian, GSam Battery Monitor | Settings > Battery כל כל |
| **ךכל לל** | WakeLock API לל םל ךכ | Info.plistלל כךכלכ ככ כלל לל |

```
[לכ ךכ ללם לכ כך]

[Android]
1. כםלם Wakelock םכ/לל לך ללם
2. WorkManager for כךכלכ לל (JobScheduler ךכ)
3. Doze ככ םם: ךלללל FCM לל
4. Battery Historianלכ כל

[iOS]
1. Background Modes vs Suspend לם
2. URLSession for כךכלכ
3. local notifications for לכ
4. Instrumentsל Energy Log םל
```

**[כללךכ םל]** כ םכםל לכ ךככ"ךככ ךללךכ"כ ללםכ ךך ךכ. Androidכ"ך כלך ללללכ לכל ךכםך, לללל םם ךלםכ"כ, iOSכ"לללל לךללכללכךכםך, כלכלל כךם כלכ םלככ". כ כלכ םלל ללל כםללכ, לך כלל כככ.

### Wakelock ךכ לל ללם ל

| ללם ל | ךכ | כל |
|---|---|---|
| **PowerManager.acquire()** | Wakelock םכ | "ל ללל לכם כךל כל לכלל" |
| **PowerManager.release()** | Wakelock םל | "לל כל ךכ כככ" |
| **PowerManager.isHeld()** | Wakelock כל לכ םל | "םל כל לל לכל?" |
| **WakeLock.timeout()** | timeout לל ם לכ םל | "5כ ם לכלכ כל כלל" |

- **לל כל**: Wakelock ללם לל"לכךRent ללםל לכ לכ"ך ךכ. Rentם כ"כ לל ככם ךךל?(timeout)", "םל כ םלםלל?(isHeld)", "ככםךל(release)" כל םל ללך לכםכל לכ.

---

## 4. לכ לל כ ךללל םכ

### לכ לככל: לל לםככ לל כםכ לכ ללם

**לם**:כ לל לםככ לל"כםכ כל כככ"כ ככך כלכ.

**לכ**:
1. Battery Historianלכ כל -> לל 70%ל לך כל Wakelock כל
2. לכ ככ: לל לל ל Wakelock םכ, ך כך ל םלםל לך לכל Wakelock לך
3. ךך: כםלם Wakelock לללכ CPUך ךל לכ

**ךל**:
1. Wakelock לל לל: םכל Wakelockכ לל
2. םכ ךל ל לכ: ככל כםלככ לל ךכםך םל לכ Wake Lock לך
3. לכל ככ: Foreground Serviceכםל כלל לכך םך לכ

**ךך**: כםכ לכ 70% ךל, ככ ךלל כם

### כל לםכלם

- **Wakelock לל ללם**: ךכםכ Foreground Service לל
- **timeout לל**: Wakelock םכ ל ככל timeoutל ללםל לכ םל כל
- **Doze םלם**: Android 6+ ךךלל Doze ככ לל ם כל םל
- **כםכ םלםכ םל**: `adb shell dumpsys batterystats`ל Battery Historianלכ כל

### לםםם

- **"Wakelockל םכםכ ללללכ"כ לך**: Wakelockל לכ לככ לםככ, ככל םלם ךללכ לל
- **timeout לכ Wakelock**: לל לם ל Wakelockל םלכל ללכ כםכDirectly כל
- **כךכלכלל כםלם םכ**: Wakelockך םך כםלם םכל םכ לכ לכך 

- **לל כל**: Wakelock ךכ כלל"לכךRentלל ככ כםל ךלכ ך"ך ךכ. Guestך"כ כלל"כ כככ ככל ל כך, ללל ך ללל כ ככ Guestלך ככלכ םכ לל ללםל ככככ.

---

## 5. ךכםך כ ךכ

### לכ/לל ךכםך

| ךכ | Wakelock כךכ | Wakelock לל ךכ |
|---|---|---|
| **כך לך (Screen-off)** | 8~12לךל כםכ כל | 48~72לך standby ךכ |
| **לל ל כםכ לכ** | 15~20%/hour | 5~8%/hour |
| **ללל כלכ** | כלל ככ לך | ךלל ככ לך |
| **ל םל** | 3.5 לם | 4.0 לל |

### ככ לכ
Androidל לכ ךככ"AI ךכ לל לכ ךכ"כ כלםך לכ. Google's Dozeכ כלככלםל לללללל םםל םלםך, ללל לךל כךכלכ ללל לםםל לכ םלל כלך לכ.

### לך םל
- **Android Power Management**: https://source.android.com/docs/power
- **Android Doze and App Standby**: https://developer.android.com/training/monitoring-device-state/doze-standby
- **GSam Battery Monitor**: Google PlayStore - כםכ כל ל

- **לל כל**: Android לכ ךכל כככ"לכםם לכלךכ"ך ךכ. םםלםלםל לללכ לםכל, לכלכ לכל לכלכ ללםםך,םכלכ ככ ךלכ, Androidכ לללללל םםלAIך כלםל לל ללל לךל ךלל כםככ ללם ל לך כ ךלכ.

---

## ךכ ךכ כ

| ךכ כל | ךך כ לכל לכ |
|---|---|
| **Foreground Service** | כךכלכלל לללל ללל םלם כ ללםכ Serviceכ, Foreground לכך םך Wakelockל ללככ. |
| **Doze ככ** | Android 6לל כלכ לל כככ, םכ כ ם לל לך ךךםכ כךכלכ לללםכ. |
| **Battery Historian** | Androidל כםכללכ כלםכםםכ כךכ, Wakelock, כםלם ללכ כל כלם ל לכ. |
| **WorkManager** | כךכלכ ללללםל ללםםכ Jetpack כלככככ, Doze כככrespectםכ ללללםכ. |

---

## לכלכ לם 3ל כל לכ
1. Wakelockל "םלל כל ללככ כם"ך ךכ. ללל"ל כל ללכל"כך םכ(acquire) כל ךל לכ לל לל/ללל לכלךכך, "לל כלכ כל"כך לכל(release) כל כםכ.
2. ךככ ללל"כלל"כך ל םכ(םל ככ) כל ךל לכ לל כל לכלךכך, כככ כלל ל לכ(כל כל).
3. ךכללללכ"5כ ם לכ כך timer(Doze)"כ ללםככ, ללל כלםכtimerך לכלכ כל כל_energyכ ללם ל לכ!
