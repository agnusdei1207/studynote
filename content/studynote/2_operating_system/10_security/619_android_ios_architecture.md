+++
title = "619. ככל OS םל (Android vs iOS לםםל כך)"
date = "2026-03-25"
[extra]
categories = "studynote-operating-system"
+++

# ככל OS םל (Android vs iOS לםםל כך)

## םל לללם (3ל לל)
> 1. **כל**: Androidכ ככל לכ ךכל ךכם םכםלכ, כלם םכללל ל ךכללך ללכ לךםכ ככ, iOSכ Apple Siliconל ךל ללםכ םלם םכםלכ, לךם כלך לךכ לכל לללםכ.
> 2. **ךל**: כ םכםל לםםל ללכ ל ךכ לכ, כל ככ, לכ ללם ככל ללל לםל כלכ. לכ כל, Androidל ART vs iOSל Objective-C/Swift כםל, Androidל םכל ככ vs iOSל ל לככל כל ךכלך ככל לםםל ם םל ללכ.
> 3. **לם**: כ םכם ככ כםלל םכלל, GPU ךל, Neural Engine םל, ללכ לך כם ךלל כםכ םם לכםך ללכ, םכם ך ללכ לל ללככ לללכ.

---

## 1. ךל כ םלל

### ךכ כ לל
ככל ללללכ לכםםך םככלל לםככםכ OSכ, PCל OSלכ ככ לםכ םכ םך, םל לכ, כםכ לכ, כםלם לךל כללכ לךכלכ.

**Android**:
- 2003כ Android Inc.לל לל, 2008כ ל לל
- ככל לכ ךכ (םלכ לכל ככלל לכם כך)
- Googleל ךכ, לםלל םכלם(AOSP) + proprietary 
- Java/Kotlinלכ ל ךכ, APK םכ

**iOS**:
- 2007כ iPhone ללל םך כל
- Darwin OS (BSD ךכ) + Apple ךל
- Appleכ ךכ כ םכלל לל
- Objective-C/Swiftכ ל ךכ, IPA םכ

### לל לםםל לל

```
[Android לםםל]


            ל כלל (Apps)               
     Java/Kotlin  (.apk)                  

     םכללם כלל (Framework)          
   Activity Manager, Content Provider,     
   Window Manager, Package Manager כ       

     Native C/C++ כלכככ               
   SQLite, OpenGL, SSL, WebKit,           
   Media Framework, Surface Manager        

     Android Runtime (ART)                 
   Dalvik -> ARTלכ כך (AOT, JIT)      

     HAL (Hardware Abstraction Layer)      

     ככל לכ                         
   Binder (IPC), Ashmem, Wakelocks,       
   Low-Memory Killer, Power Management     



[iOS לםםל]


            ל כלל (Apps)               
     Objective-C/Swift  (.ipa)             

     Cocoa Touch (םכללם)              
   UIKit, Foundation, Core Data כ       

     םל םכללם                       
   Core Animation, Core Graphics,          
   AVFoundation, Core Audio               

     Darwin (BSD ךכ) + XNU לכ          
   Mach םם, IPC, כככ ךכ            

     ככלכ כ םכלל ללם          

```

**[כללךכ םל]** Androidל iOSל לםםלכ"ךכ לך"ל כלם ל לכ. Androidכ ככ לםל ככ(ככל לכ)לך ללל לםל כך כל ךככ"ללכם"ך ךכ. iOSכAppleל לל לךם ךכללAppleל כךכ ללםכ"לםם"ל ךכ.

- **לל כל**: Androidל iOSל ךךכ"םלל ככ ךל לל"ך ךכ. Hamburgerכך םכ ככככל כךםל כלם, םלל ככ ךלכ, לכםם OSכך םכ(ללל םל)ל כלםכןלך לכ.

---

## 2. לםםל כ םל לכ

### Android ART vs iOS Objective-C/Swift כםל

**Android ART (Android Runtime)**:
- Dalvik כלםלככ לםםכ כללל כל
- AOT(Ahead-of-Time) לםל: לל ל לםל -> לם לכ םל, לל ךך כ לל
- JIT(Just-In-Time) לםל: לם ל םל כככ לםל
- 2017כ Android 7כם Profile-Guided Compilation (PGC): לל ללםכ לככ AOT

**iOS Objective-C/Swift Runtime**:
- Objective-Cכ כל כלל לכ כל (Smalltalk )
- Swiftכ כ לל םל ללם + לך ללם
- AOT לםל (Swift)AOT ככ interpreter
- iOSללכ ככ לל ככ לםלכל ככללל לל

```
[Android ARTל לכ כל]

לל ל:
 APK כ Dalvik כלםלכ (.dex)
         
         
    dex2oat (AOT לםלכ)
         
         
    לםלכ ךךל (.oat) -> ללל(לל ךך כ לל)
         
         
    לם ל:
    
     Profile-Guided Compilation   
     לל ללםכ כלכ: AOT לכ 
     ככל: JIT (לם ל לםל)  
    

[iOS Swift/ObjC Runtimeל לכ כל]

ל לל ל:
 Swift/ObjC לל לכ
         
         
    Xcodeלל ככ לםל (AOT)
         
         
    ךךל לכ -> ל ככ
         
         
    לם ל: ךךללללם (ךכ םל םל לל)
```

**[כללךכ םל]** Androidל ARTכ"לל ככ"ל כלם ל לכ. לכ(כלםלכ)כ ךללל םלם כם ךכךכ לכל לכ ךלל(JIT)םךכ, לל ככ(AOT)םל ךלך ל לכ. iOSכ"ללכלל לכלם"ך ךכ. ךללל ככלככל ללל, ללכללל כככ(לם) ככ כל ל לכ.

### םכללל כככ ךכ כך

| םל | Android | iOS |
|---|---|---|
| **כככ ךכ** | Low-Memory Killer (OOM Killer ךכ) | Jetsam (כככ לכ ל םכלל לכ) |
| **לםכם ללם** | Activity, Service, BroadcastReceiver כ | App Extension, Background Modes |
| ** IPC** | Binder (לכ ככלכ) | Mach םם (XNU לכ כ) |
| **כל ככ** | םכל לל, ל לכ, SELinux | ל לככל, לכ לכ, Hardened Runtime |
| **כךכלכ לכ** | WorkManager, JobScheduler | BGTaskScheduler, Push Notifications |

### כםלם כ לכ ךכ

**Android**:
- Wi-Fi/Mobile כלם לם: ConnectivityServiceך ךכ
- Doze ככ: ללך כלל ל כךכלכ םכ לם
- App Standby Bucks: ל לל ככל ככ לכ םככ לל
- כלם לל ככ: כךכלכ כלם לל לם

**iOS**:
- ללכ ככ: לל ללם ללם
- Background App Refresh: לככ כלם לל
- Apple Push Notification לכל (APNs): םללל םל
- Wi-Fi ללם: Intelligent Hotspot ךכ

```
[Android Doze ככ כל]

[לכ לם]
לל ללכך כךכלכ לל לם
-> כםכ לכ: כל

[Doze לל]
םכ כך ללךל לך ל ם + לל לך ךך
-> ככ כךכלכ לל לם
-> כםלם לך לם
-> לכ/JobSchedulerכ לכ םל
-> כםכ לכ: כל כל

[Exit Doze]
ללל(ךלכ לל), םכ לל, ללך לך
-> לכ לםכ כלל
```

**[כללךכ םל]** Doze כככ"םלל לך ככ"ל ךכ. לכל ללכ(ללל כלל) כל כך(כךכלכ לל לל), םלם(לכ/םל)כםךלך, לכל לכ(ללל/םכ ל) ככל(לכ לם)םכ.

- **לל כל**: ככל OSל לכ ךככ"ךלל לם"ך ךכ. כל ככ לכ(Doze) לכ, ללל, TV כל כך, ךל לךל כל לככ לך, לללכ ככ םלםםכ.

---

## 3. לם כך כ כךכ כל

### Android vs iOS: ךכל ךלללל םל לל

| םכ | Android | iOS |
|---|---|---|
| **ךכ לל** | Java, Kotlin | Objective-C, Swift |
| ** IDE** | Android Studio | Xcode |
| **כם** | APK, כלם ל לםל ךכ | IPA, App Storeכ לל כם |
| **םכלל כלל** | כלם ללל, לל, םכ םך | Apple לל, לםכ ךך ל |
| **ללל םך** | לל, כל ל, םל ךל ללל | לךכ UX, ךכם םכלל םם |
| **כל** | םכל ככ, SELinux, OTA לכלם לל ךכ | ךםכ לככל, ככ כל םל |
| **ךכ כל** | כלם ךך םלם םל | לםכ ךךכ םלם םלל |

```
[םכם לם ךל]

"כלל + ללל לל" לל -> Android
- כלם ךךלל לכםכ ל
- םל ללם לך, לכ ל לכ
- לכ ל לםל כם

"לךכ םל + כל" לל -> iOS
- םככל ללל כל
- לךם כל לך
- Apple לםך (Watch, iPad, Mac) לכ
```

**[כללךכ םל]** Android vs iOS לםל"לל לל לכ"ך ךכ. Hamburgerכ םככ, כככככ"כלם לכל ככ כלם ככ, כלם כל"לל ךלםך, כךםל"לךכ םל, םככל לכלכ םל ךךל ךכ"םכ.

- **לל כל**: כ םכםל ךךכ"לכל כככ"ל ךכ. Androidכ Hyundai/Kiaלכ כלם לל, כלם ךךככ כךכ ם ל לך םך, iOSכ Genesisלכ םל כךל ךךלך כלכ ךםל לךםכ.

---

## 4. לכ לל כ ךללל םכ

### לכ לככל: םכל םכם כלל ל ךכ

**לם**:כ ךלל Androidל iOS ככלל לכםכ כלל לל ךכםכך םכ.

**ךכ לם**:
1. לכ(םל): Firebase Cloud Messaging(FCM) vs APNs
2. כםלם: לל כ HTTP/2, WebSocket לל ךכ
3. לםם: לל כ End-to-End לםם לל ךכ
4. לםכל לל: SQLite(Android) vs Core Data(iOS) -> ךם SQLite לל ךכ
5. ככל לכ: לכל כללל, לל כ ככלל ככ לכ םל

**כל**:
- React Native ככ Flutter םל: םכל לכ כללכ לל כל
- כלםכ ככ: םכםכ ללםך םלם ךלכ ככ ךכ

### כל לםכלם

- **כל םכם ךל**: Android/iOS/כ כ? ללל לך לל לכל ככ
- **ךל לם לם**: כלםכ vs םכל םכם (React Native, Flutter)
- **םכלל םל םל**: םכ םך, כככ, GPU לכ כ
- **כל לך**: ךללככםכ, GDPR כ ךל לל

### לםםם

- **"ךל לככללכ ללם כל ךכ" ךכ**: םכםכ UI/UX ךלככלל ככככ, כלם לככללככ םכםל כך לל םל
- **Androidללכ םלםםך iOS כם**: ככל ךלכ כלךל. םכםכ ככ כלל לל ל לל

- **לל כל**: םכל םכם ךכל"םל לם"ך ךכ. םךלל לל, כ ככלל ךל לל ללככ, לל כ לל ךכם לכלל לםלל לםםל םכ. ךככ"socks"ך" tjfk"ל לללכ ללם ככל כ ככלל כך ללםל םכ.

---

## 5. ךכםך כ ךכ

### םכםכ לכך

| ךכ | Android לל | Android כל | iOS לל | iOS כל |
|---|---|---|---|---|
| **לל** | כל ללל, כלם ללל | םכם םםם | כל כך ללל | לםכ ללל |
| **ךכ** | כלם ךך םלם ךכ | םלם כל | לםכ ךךכ םלל | Apple ךכל כל |
| **לל** | ךך ךכ לכ | ךכ לםל כל | ךכ לםל כל | ךכ ךכ לכ |
| **כל** | לםלל, םכל | לכלם לל ךכ | ככ םל, לךם לככל | םל ל כל לל |

### ככ לכ
Androidל iOS ככ ARM ךכלל Apple Siliconלכ לל לך לל םם כלםך לכ. כם AI/ML םם(Androidל TensorFlow Lite vs iOSל Core ML), לל ךכ ךם, םכם ך לכל כל ככ כםלכ.

### לך םל
- **Android Open Source Project (AOSP)**: https://source.android.com
- **Apple Developer Documentation**: https://developer.apple.com
- **Google Play Console / App Store Connect**: ל כם כ כל

- **לל כל**: כ םכםל כככ"לךם"ל ךכ. לל ךךל לללך(םכם ך ךכ לל לל), ככ ךלל (םל)כ ללםכלכךכ jzyk(םל ךכ)כ ךלםך כ ךלכ.

---

## ךכ ךכ כ

| ךכ כל | ךך כ לכל לכ |
|---|---|
| **ART (Android Runtime)** | Androidל לםכללל לם םךלכ, Java כלםלככ ARM ךךלכ כםםכ לםלכל כםללכ ךלככ. |
| **Cocoa Touch** | iOSל לל םכללםכ, UIKit, Foundation, Core Data כל םםםכ ל ךכל ךכלכ. |
| **Binder** | Androidל םכלל ך םל(IPC) כלכללכ, לכ ככלכ ךכלכלכ IPCכ לךםכ. |
| **XNU לכ** | iOSל macOSלל ללככ לככ, Mach כלםכלכך BSDל לםלכ. |

---

## לכלכ לם 3ל כל לכ
1. Androidל iOSכ "ככ ךלל כלם"ל ךכ. Android כלםכ לכ לכם(ךך)כ לך כלל ל ללכ, iOS כלםכ לםל לכם(Apple ךך)כ לך כלל ל לכ.
2. Androidכ כלםלל כלך כלככ ל ללכ(ללכ כל), כךך לכםכ ללל ללכ ל לך(כל לל ךכל), iOSכ כלם ךלל לךםל(לככל) םםך כלכ ללך לך לםככ.
3. ךככ כ כלםל כלל ךכ! לךכך Communicationםך(כלל), כך(ךל), ךכל ךכך(ךכם), ךכל ללםכ ך(לל)לכ!
