+++
title = "607. TPM (Trusted Platform Module) כ ככל כל"
date = "2026-03-25"
[extra]
categories = "studynote-operating-system"
+++

# TPM (Trusted Platform Module) כ ככל כל

## םל לללם (3ל לל)
> 1. **כל**: TPMל ככככלכ ככל ככל כל ללכ, לםם םכ םכללללכ לל לל ךכםל לםםלל ךך(כםם, םכך)לככם םל ככ(Disk Encryption Key, ללל)ל ךכםכ לכל ךכלכ.
> 2. **ךל**: TPMל כם ךללל םללל ללללל כךלל ללםל, לללל כככםל ככל כלל ככ כלםכככ םלל ככל ללל לככ כםםכ ךכםכ םכלל ךכל לךל כללל לךםכ.
> 3. **לם**: TPMל לכ לל(Root of Trust Measurement)ל BIOS/UEFI כל כם(Secure Boot)ך ךםכל, לככל לל כםכככ לכל לל לכםך, BitLocker כ כלם לםםל לככל TPMל ללכ םכ ככ כלם םכ כםםכ לכ ך כל ללל ללםכ.

---

## 1. ךל כ םלל

### ךכ כ לל
TPM (Trusted Platform Module)ל PCכ לכל ככככל ככ כללכ כלכ כל ל כל ללכ, TCG (Trusted Computing Group)ך ללם ךל םלל ככ ללככ. TPMל כל ללך, SHA-1/SHA-256 םל לל, RSA/ECC לםם ךלך, לל 16KBל ככל כםכל כככך לכ לם כלםכלםכככ ךלככ, םל לככ לםם םכ לכ ל לככ לכםל לך ככללכ ללםכ ךלכ. ל םל ככל TPM ככלל ללכ םכ TPMל ככללכ םךכל לכ ם לםםלל ךךלכ כלם ל לכ לםםל ללך ככ.

**םלל כ כל כך**
לםםללכלככ ללם כלל כלם ל לכ ךכל םךך לכ. לל, ככ לםםללכ כככל כככל לםכככ, ככככ לל ל לכ ךם(ל: לכ כם ךם)ל םכם ךךלכ ככ םכ םכלכ ללם ל לכ. כל, כם ךללל BIOSכ כםככך ללכ ךל, ללללך לככ ללםכ ךלכ כלכל ללכ כךלכ ךלכ. לל, AES םכ ללללך כככל םכלכ לכככ, cold boot attackלכ RAM כלל םכ לל כךםל םכ כלככ ככל ךךל ךכםכ. ל ל ךל לםםללל םךכ כלל ךםםכ םכלל ללל ךכ ללך םלםך, TPMל ך םכלכ כלםכ.

```
[TPM vs לםםלל לל לםםל לם ככ כך]

[לםםלל לל לםם (ל: VeraCrypt)]
- כלם לםם ם(DEK)ך AESכ כםכ
- BUT: כם ל OSך DEKכ RAMל םכלכ ככם
- ךך ךכ: כםל כככ םל / כםככ לל ךל

[TPM + BitLocker לכ לםם]
- TPMל Volume Master Key(VMK)כ ככל ללםך כך
- VMKכ TPM לככ םכ לכ כך
- כם כךל לל(PCR)ל לךםלכ VMKך םלכ

[כם ךלל ככל כךל לל םכ]

BIOS/UEFI --> לל --> PCR[0]ל כל םל לל
     |
     v
Bootloader --> לל --> PCR[1]ל כל םל לל
     |
     v
Kernel --> לל --> PCR[2]ל כל םל לל
     |
     v
PCR ךל לל כככ "לל לם םל"ל כך!
     |
     +-- לל --> TPMל VMK םל --> OS לל כם
     +-- כלל --> TPMל VMK כם --> כםם ךכ!
```

**[כללךכ םל]** ל ךלכ TPMל ל "לכל ךכ(Root of Trust)"לכ כככלכ כללכ. TPMל ללל לל ככ ךל ךלםכ ךל לככ, כם ךללל ך כך(BIOS --> Bootloader --> Kernel)ך לםכך ללל םכ לםםללל םל ךל PCR(Platform Configuration Register)ל כל ללםכ. BitLocker Recovery, TPMל VMKכ ככלככ ללל כללכ PCR ךללםכ לל לםל םלל םל PCR ךל כךםכ. כל םלך BIOSכ כלםךכ כםםל לכל ךלכלככ PCR ךל לל םלל ככלככ, TPMל VMKכ לכ םלםל לככ. לךל לםםללכלככ כלם ל לכ םכלל כלל ככל כללכ.

- **לל כל**: לםםלל לםםכ ךך כככםכ ל לל לכלככ כךכ ל ל לכ ךך לכלך ךכ. TPM ךכ לםםכ ךך לל ככ לכלך םכ כ ללל ךך כל לך לל "לך כ כלל ל לכ לכל לל לללך?"כ ךךך לל םלםכ ךלכ. לםםללכ לל ל ללכ, לל לל ל לכ.

---

## 2. לםםל כ םל לכ

### TPM לל ככ ךל לל

TPMל כל ל לל לכ כל ךכל לםכ לם כלםכלםכככ.

| ללכ | לם | ככ כל | כל |
|---|---|---|---|
| **RSA/ECC ךלך** | ךךם לם לל ךל | TPM ככלל ם לל, לכ, ךל לם (ם םכל ל לככ כלל לל) | ךך ככל לכ כככם ללך |
| **SHA-1/SHA-256 לל** | םל לל ךל | כם לל ךלל HMAC כל ךל כ PCR ךל | כל לכ לל |
| **RNG (Random Number Generator)** | לםםללכ ללם כל לל | TPM ככ entropy source ךכ ם לל, nonce creation | לללכ ךככ כלל ללך |
| **NVRAM (Non-Volatile RAM)** | לך ללל | Endorsement Key, SRK, storage ם, PCR ךל ככל לל | ךך לל כלל לל |
| **PCR (Platform Configuration Register)** | כם כךל לל ך לל | 24ךל 20כלם כללם (TPM 1.2 ךל), ך כךכ םל כל לל | לך לל כל לם לך םלל |
| **Endorsement Key (EK)** | TPM לל ל כלכ ךל RSA ם | TPM לם לכ, remote attestationל לל | לכככלל כלכ ללל |
| **Storage Root Key (SRK)** | ללל םל ללל ככ ם | TPM ללל לל ל 2048-bit RSA ללכ לל, master key לם | ךך Master לל |

### TPMל םל cryptographic operation: Sealך Unseal

TPMל ךל כללל םלל "כלםכ TPMל כל(Seal)םך, םל לםללכ םל(Unseal)םכ"כ ךלכ.

```
[TPM Seal / Unseal כלכלל ככ כל םכ]

[Seal לל (כלם כל כך)]

Owner: "BitLocker םכ TPMל כלםל"
         |
         v
TPM ככ כל:
  1. כל ללךכ כל ם(DEK) לל
  2. DEKכ TPM ככ RSA לללכ לםםםל NVRAM לל
  3. DEKל כםם לך(PCR ך: לל כם םל)ל םך ךכ
  4. DEK םכל לכ TPM לככ לככל לל!

[Unseal לל (כלם םל כך)]

כם לכ --> PCR[0~7]ל לל כם כל םל לל
         |
         v
OSך BitLockerלך "כםםםל"כך לל
         |
         v
TPM ככ:
  1. םל PCR ך vs כל כל PCR ך כך
  2. ךל כל --> DEK כםם (Unseal) --> OSל לכ
  3. ךל ככ --> כםם ךכ! (ךך ךל)

םל: PCR ךל םכככ כככ TPMל DEKכ לכ ככל לל
```

**[כללךכ םל]** Seal/Unseal כלכלל TPMל כל לםל ךל ל כללכ לללכ. לכלל לםםלל לםםללכ "כככםכ כלכ כםם"ללכ, TPMל "כככם(ם)ל םך םל ללם לם(PCR)ך כל ללך כלםל כםם"ככ לךכ כל ככל ךםםכ. כל םלך BitLockerכ לםםכ כםPCל SSDכ כל ככ PCל לךםכ, םכ PCל TPMל לכ כם לל ךל ךלך לל ללככ VMKכ לכ םלםל לככ. PCR ךלללללל כךםכ ל כלל, םלל ככל ללךל ךלםכ "לם לל כל(Stateful Security)"ל םל לככ.

### Endorsement Keyל Remote Attestation

TPMל כ ככ ללם לםל remote attestation, ל "ל ללםל םל ללם לםלל לך לכל לכםכ ך"לכ. לכ ךכםך םכ ךל Endorsement Key (EK)כ.

TPM manufacturing ל ךללל ךככ 2048-bit RSA ם ללכ, TPMל לככםל bindingכל לל TPM ללללל cryptographicםך לכםכ לכל לםל םכ. EKכ TPM לככ export כךםכ, EKל ךלםכ לכ TPM כלכ כך ל לכ.

```
[Remote Attestation (לך לכ)ל לל םכ]

[כך 1: AIK (Attestation Identity Key) לל]
ללל PC --> TPMלך "AIK ללםל" לל
TPM: EKכ ללםל AIKל לכ ם, AIK ךךםכ לללכ כך

[כך 2: כם כךל לל ך לל]
כם ךללל PCR[0~7]ל כלכ םל ךל AIKכ לכ
לככ PCR ך = "ל PCכ םל ל לםםלל ךללכ כםכ"

[כך 3: לך ךל לכל לכ]
לככ PCR ך --> לך לככ לל
לך לכ:
  1. EK ללל ךל (TPMל םל)
  2. לככ PCR ך ךל (כל םל)
  3. PCR ךל known-good baselineך כך
  4. ללםכ "ל PCכ ללםככ" םכ

םלל:
- ךל VPN לל ל ללם ךל לך OSלל ךל
- לכל לם לל ל םכך לכ ךכם םךלל ךל
- םכלכ VMל ללכ כ לככ כלל לכלכ ללםכל
```

**[כללךכ םל]** Remote attestationל "לכם hardwareלל לכם softwareך לםכך לכ"כ ללל ל3ל(לך לכ)ך cryptographicםך ךלםכ םכםללכ. םלל EK (Endorsement Key)ך TPM לל manufacturing כךלל ךככTPMללכ ל לככ ללכ. ככל םלך OSכ כםםלכ ללללכ, לך לככ PCR ךל לכ ךל ךללל לכ ךלם ל לכ. ל ךללל (Zero Trust) כםלםל םל ךל ללכ, "ככ כםלםל לכ = לכםכ"כ לםל ךלל לךםכ.

- **לל כל**: TPMל לםם לךל לכככלך ךכ. לכככל(Endorsement Key)ל ךלך לכללכ(לם TPM), לל לכ(AIK)כ ככ ל לך, לל לככ ללםכ "לכ ללכלללללך(PCR כךל)"כ כלל םלםל, לל כללכ כל ככ ל םכככ ללכ ךכ ללל לכםכ.

---

## 3. לם כך כ כךכ כל

### TPM כלכ ךכ כך (TPM 1.2 vs TPM 2.0)

| כך םכ | TPM 1.2 | TPM 2.0 |
|---|---|---|
| **לםם לךכל** | RSA 2048-bit, SHA-1 (ךל) | RSA 2048 + ECC (P-256, P-384), SHA-1/256/384 (לךכל לם ךכ) |
| **PCR כללם ל** | 24ך (PCR[0~23]) ךל | 32ך לל (ככ םל ךכ), כל םל |
| **ם ךכ** | כל hierarchical ככ (EK --> SRK --> Storage) | ללם hierarchical ככ (Primary Seed, Platform Seed) |
| **ךם ךכ** | כל owner password כל | כלם authorization session ךל (HMAC, policy session) |
| **לךכל כלל** | SHA-1ל לךלל ללל כל ל לךכלכ כך | לךכלל software updateכ ךל ךכ |
| **כלל** | PC/server םם | PC, server, IoT, embedded system ככ כל |

TPM 1.2כ 2000ככ לכ לךכ, SHA-1 םל םלל לךם לללל כךכ לםלכ םכללך ךלכל לל לךכלל לכלםם ל לכ ךל םךלכ. TPM 2.0ל לךכלל firmware updateכ ךלם ל לכ algorithm agilityכ כלםל, SHA-1ל לללל כךככ SHA-256לכ לךכלל לםם ל לכ.

### TPMך ךל ךל (Intel SGX, AMD SEV)ל כך

| כך םכ | TPM (לל ככ) | Intel SGX (םכלל ככ) | AMD SEV (םכלל ככ) |
|---|---|---|---|
| **כם כל** | כם כךל, כלם לםם ם, ללל | application memory region (Enclave) | entire VM memory |
| **כם ככ** | ללם לל (OS/BIOS םםם לל םכם) | application כל (ל ךכלך כלללכ Enclave לל) | VM כל (ךלכל לל memory) |
| **ךכ כל** | ככל ככ ל (לל) | םכלל ככ ךכ כככ (PRM, Processor Reserved Memory) | AMD םכללל כככ לםם לל (MSE) |
| **לל לככל** | BitLocker, secure boot, certificate storage | ככ ךל (secure computation), AI inference on encrypted data | cloud VM encryption (VMל כככ ללכ hostלךכ לך) |
| **ככל ךך כל** | TPM ל ככל םך םל (לכל ךם) | cold boot attackל כם vulnerable (כככך CPU package כככ כלך) | כככ לםםכ cold boot attack כל, but hypervisor לכ םל |

```
[כל כללכ protection scope כך]

[ךל כל כם כל] TPM 2.0
  [Platform: BIOS --> Bootloader --> OS --> App]
  TPM: ל ךך כךל לל + ם ךכ

[לך כם כל] AMD SEV
  [ךלכל memory לל]
  SEV: VM <--> Host (םלםכלל) ך כככ לםם

[ךל לל כם כל] Intel SGX
  [Application ככל Enclaveכ ךכ]
  SGX: םל sensitive לכ/כלםכ Enclaveל ךכ

ךכ:
- םכם לכל לכ ךכ --> TPM
- VM כלל ככ לל --> AMD SEV
- לםכללל כלל ככ ךל --> Intel SGX
```

**[כללךכ םל]** ל ךלל לם כםללל לךללכ לכםכ. לל ךך כל ללםללכ TPMל ללםל כם כךלל ךלםך, ך לל לםככ VMל AMD SEVכ כככ ככ לםםכ ללםכ, VM ככל כל כךם לכ(ל: AI ככ inference)כ Intel SGX Enclave כלל לםםכ כל כל לכל לםכ.

- **לל כל**: ל ךלל ךךכ ל ללל ככ ללםך ךכ. ל ככ ללם(TPM)ל לל כלל ךלםך, כfur ךךכ ךל ךל ללל כםםכ, כ ככ ךךכ לכ ךלללכככל כםםכ. ככ ךל םך לכם כ ךל ללם לםך ככ.

---

## 4. לכ לל כ ךללל םכ

### לכ לככל: BitLocker TPM-only כםם לם vs TPM+PIN לל כם

**לככל לם**:כ ךלל כםPCך BitLocker TPM-only כככ ללכל לכ. IT ךכלכ "TPMל ללכך לך לל לל OSכ כםככ לכלכ כםם"כככ ללםכ.כ כ, ללכלל כםPCך כככלכ.

**ללכלל ךכ**: ככל כםכל לכ TPMל PCR ךל ללםל כםככ כםםכל לל ךלכ.

**לל ךך**: ככל כםכ SSDכ ככל ככ PCל לךםךכ, TPM לל unsolderingםל כל ככ כםכל TPMך ךםםכ? ל ךל PCR ךל כל לל לללכ ללכל BitLocker VMKך םלכלכככ!

**כלל םל**: TPM-only כככ "לככ hardwareלל כם"ךלכ םלםך, "לככ לכל כם"ללכ ךלםל לככ.

```
[BitLocker לל כככ כל לל כ ךך לככל כך]

[ככ 1: TPM-only]
כם לל: םכללכ םל, לל לל כםל
ךך ךכ: TPM swap --> BitLocker לם ךכ!
כםם לך: PCR[0~7] לל + לככ hardware

[ככ 2: TPM + PIN] (ךל)
כם לל: hardware + לל לל כל ךל
ךך ךכ: TPM swap + PIN ככםםל םל
כםם לך: PCR לל + לככ hardware + לככ PIN

[ככ 3: TPM + PIN + Recovery Key (escrow)]
כם לל: לם םכ םם
לל ךל םךללכ Recovery Keyכ ADל escrowםל
ךכלכ כך ךכםככ ללםכ ךל לכל
```

### כל לםכלם (ךל םך TPM כל ךם)

- **TPM + PIN םלם**: BitLocker GPO(Group Policy Object)לל "Require authentication via startup PIN" ללל םלםםל hardware theftל לם BitLocker לםכ לל לכםכך?
- **Secure Boot כךל ךל**: UEFI BIOSלל Secure Bootכ םלםםך, Microsoftלל לכם כםכככ םלםכ ללל ללםכך?
- **TPM 2.0 לךכלכ ךם**: כךל TPM 1.2 ללםל SHA-1 ללל כלל לם TPM 2.0לכ ךלםךכ firmware updateכ ללםכך?
- **לם כך לככל**: TPMל ךל כךכ ככככך ללכלל כ, BitLocker Recovery Keyכ ADכ Azure ADלללםכלכך?

### לםםם

- **TPM-onlyלכ ללםך Secure Bootכ כםלם**: TPMל PCR ךל ךכלכ םכ םלםלכ, Secure Bootך ללכ לל לככ לל PCR ךל ללם ל לכ. ל, לכ כםםל ללםל ךל כככככ PCR ךל כלםל לךכ BitLocker םכ ךכל ל לכ ךל ךכך לךכ.
- **TPM לל כםלםםך כככםכ לל**: לכ לללל לםםלל לםם כלל BitLocker password-only modeכ כלךכ ךלכ, cold boot attackל לם RAMלל AES םךכ לםל כל לךכ.

- **לל כל**: ככ ללם(כל לםםלל)כ לך כלכ(TPM)ל לךם לך ךכ. hardwareל ללכ כלכל לל לכ(כםככ כל)ל םם ל לל ךך לל(Disk Encryption Key)כ כככ ל לכ. ככל hardwareך(TPM+PIN)כ םך ללםל ללם ככל ככ.

---

## 5. ךכםך כ ךכ

### לכ/לל ךכםך

| ךכ | TPM כלל (לםםלל לםםכ) | TPM 2.0 + Secure Boot + BitLocker |
|---|---|---|
| **לכ לל כל** | כםככ לל ךללכ םכ ם םל ךכ | כם ךללל לל כל ךל ל כםם ךכ |
| **לל כלם כם** | SSD םל ם ככ PC לך ל םכ כל | SSD םל ם TPM כללכ כםם כך |
| **לל לכל** | כככם לל ל 100% לם | hardware (TPM) + לל(PIN) לל לל |
| **לם כל** | ם םל ם כלם לל לל כל | לל כם ל temp keyכ םל, ללל לכ לל כל |

### ככ לכ

TPMל PC םכםל םל כל ללכ לכ לללכ, IoT כ edge computing םךללכ ללםלל ככ. 2024כ לם NIST SP 800-193 ("Platform Firmware Resilience") םלל כך לםך םך, ככ IoT ככלללכ TPM-Lite ככ fTPM (firmware TPM)ל םלםכ ךל ךל לךלכ םככך לכ. םם לללם לכל, לכךך, לל לל ללםללכ "כם כךלל כלכל לל לככ כלל ךכםכ"כ fail-secure ללל כל לכםככ םכל ךלםכך לכ.

כם TPM 2.0ל לךכל כללל, Post-Quantum Cryptography לכל RSA/ECCכ PQC לךכללכ ךלםל ם כ, םכלל ךל לל TPM firmware updateכלכ כלם ל לכללךכ ךכםך םכ.

### לך םל

- **TCG (Trusted Computing Group) Specification**: TPM 1.2 / TPM 2.0 ככל ללל
- **ISO/IEC 11889**: TPMל ךל םל
- **NIST SP 800-147**: BIOS Protection Guidelines
- **NIST SP 800-193**: Platform Firmware Resilience

- **לל כל**: TPMל כלם לךל לכככלך ךכ. לכככל(TPM)ל ללכ לל לכ(AIK)כ ככ ל לך, כל ללל לכם ל לכ. ל לכככלל כלם ללכ םלםכ ךל לככ, לכ כ לם(כם כךל)כ םלםך, ככ ךל לללכ כל(ם ךכל)לך ככךך ללכ ךכלך, םכככ ללםכךך כל ךך כלככככם ךכללכ.

---

## ךכ ךכ כ

| ךכ כל | ךך כ לכל לכ |
|---|---|
| **Secure Boot** | TPMך לכםל לככל לל כםככל לכל לםל UEFI םלל לללל לל לכםכ םכלל-לםםלל ךם כללכ. |
| **BitLocker** | TPMל Seal/Unseal כלכלל םלםל OS כם ל ללם כךלל ךלםך, ךל לך ללכ VMKכ םלםכ Microsoftל ככ לםם לכללכ. |
| **PCR (Platform Configuration Register)** | TPM ככל 20כלם כללםכ, כם ךללל BIOS, Bootloader, OSל םל ךל ללללכ כל ללםל םכםל כךל לםכ cryptographicםך ךכםכ. |
| **Endorsement Key (EK)** | TPM לל ל ךללל כלכ 2048-bit RSA ם ללכ, TPMל לכ כ Remote Attestationל cryptographic identityכ ללככ. |
| **Intel SGX / AMD SEV** | TPMל םכם ללל לככ ךכלכ םכ ככ, SGX/SEVכ םכלל ככ ככ VM כככ ללל application כל ךככ לךםכ ללכ םכלל כל ךללכ. |

---

## לכלכ לם 3ל כל לכ
1. TPMל לםם לל לכ ככ ללך ךכ. ל ללל ללכ לך כ ל(םכלל ל)ל לךכלל, לככ ככם םלך לםםללכ ללכ "ככ כ כ לללכ ללכ ל ךל!" םך לכ כלכ כללל ללל.
2. ךככ ל ככ ללל ךכ ככךככ ללכ לל לכ ך לככ, לל "לכ ל ל(לםם)ל ךךםך לללכך(כם כךל)"כ ךךם לםך, ללל ללכ לל ל ךלל לךל ךלכ כךםל, םכככ כככ "ל כ! כךך לל ךלכל!" םך כםם םכ כללל ללל.
3. ךכל ללכ כלככ ל ךל ללך ככ כלל םכ. לככHardware(TPM)םך לככSoftware(לל PCR)םך לכככככם(PIN)ככ ל ךל ללך ככ כלל ל כ(כלם)ל לככ ללכך לכם כל ללםללל!
