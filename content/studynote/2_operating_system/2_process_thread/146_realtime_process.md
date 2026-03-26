+++
title = "ללך םכלל"
date = "2026-03-22"
weight = 146
[extra]
categories = "studynote-operating-system"
+++

# ללך םכלל (Real-time Process)

## . ללך ללם ךכ

### 1. לל כ םל

ללך ללם(Real-time System)ל לל ךךך ככל לךך ךככ לל(Timing Constraint)ל כלםל םכ ללםלכ. כלם "ככ" ללםל לככ "לל ךכם לכ לך"ל כלםכ ךל םללכ.

> **כל:** לכ ללםל "ךכם ם ככ" ככםכ ככללך, ללך ללםל "לםם 30כ לל" ככל כלםכ ככללכ.

```
 Real-time vs General Purpose 
                                                     
  לכ ללם (Best Effort):                         
  Task A: 50ms  (ככ לכ, ככ לכ)         
  Task B: 200ms  (םךל לכ)                   
  Task C: 1000ms  (ךכ לל ככ)                
                                                     
  ללך ללם (Guaranteed):                        
  Task A:  10ms  (םל 10ms לכ)               
  Task B:  50ms  (ללל ךלכ כל)            
  Task C:  100ms  (כככל לל)                 
                                                     

```

### 2. םכ ללך vs לםם ללך

| ךכ | Hard Real-time | Soft Real-time |
|------|----------------|----------------|
| **כככל** | לכל לל םל | ךל, ךכ לכ םל |
| **לכ ךך** | ללם/לכ לך | לכל םל לם |
| **לל** | םךך לל, לכל ABS | כלל לםככ, לכל ךל |
| **OS** | VxWorks, QNX, RT-Linux | לכ Linux, Windows |

```
 Hard vs Soft Real-time 
                                      
  Hard:                               
  Deadline |X|        
                  לכ (ככל)        
                                      
  Soft:                               
  Deadline |||X|||      
            כככ לכ (ךכ כלכ OK)
                                      
  General (Best Effort):               
  Deadline ||X||     
            לל ככל ככ            
                                      

```

## . POSIX ללך לללכ

### 1. SCHED_FIFO (First In, First Out)

ללך לללכ לל ל ךל כלם כללכ. כל ללללללכ םל כלם ללככ לםככ, לכללכ לכ(yield)םךכ ככםכ כךל לםל ךלםכ.

```
 SCHED_FIFO כל 
                                           
  לללל: RT-99 > RT-50 > RT-10         
                                           
  לך >      
                                           
  RT-99:  (ךל לם)       
                                          
           yield/block לל                
                                          
  RT-50:         (לם)            
  RT-10:               (לם)          
                                           
  םל:                                      
  - ללכםל לל (כל/כל לללל)    
  - כל ללללך לל לל               
  -(Starvation) ךכל                  
                                           

```

### 2. SCHED_RR (Round Robin)

SCHED_FIFOל כלםלכ, כל ללללל םכלל ךל לך םככ(Time Quantum)ל ךללכ לםםכ לםככ.

```
 SCHED_RR כל 
                                           
  לללל: RT-50 (כל)                   
  Time Quantum: 10ms                       
                                           
  לך >        
                                           
  Task A:              
  Task B:              
  Task C:              
         |<--10ms-->|                       
                                           
   = לם,  = כך                 
  כל לללללל כלכ ככ לם        
                                           

```

### 3. ככל לללכ לל כך

| לל | לללל כל | לל | לך םככ | לכ |
|------|---------------|------|-------------|------|
| **SCHED_FIFO** | 1~99 | כל ךכ | לל | םכ ללך |
| **SCHED_RR** | 1~99 | כל ךכ | לל | לםם ללך |
| **SCHED_OTHER** | 0 (nice) | CFS ךכ | CFS ךכ | לכ םכלל |
| **SCHED_DEADLINE** | - | EDF ךכ | לם לל | לל ללך |

## . ללך לללכ לךכל

### 1. RM (Rate-Monotonic) לללכ

לךך לל םלםל כל ללללכ םכםכ **לל לללל** םכ לךכללכ. כל םכלללל ללל לל םכ ככלכ לככלכ.

```
 RM לללכ ל 
                                             
  Task-1: לך=10ms, לםלך=3ms  (P:ך)  
  Task-2: לך=20ms, לםלך=4ms  (P:ל)  
  Task-3: לך=50ms, לםלך=8ms  (P:ל)  
                                             
  לך >  0  3  6  10 13 16 20 23 26 30   
  T1:    [===]   [===]    [===]    [===]    
  T2:        [====]       [====]            
  T3:            [========]                  
                                             
  CPUלל = 3/10 + 4/20 + 8/50 = 0.74     
  םך: U  n(2^(1/n) - 1)                  
       (n=3: 0.779, 0.74 < 0.779 -> ללל ךכ) 
                                             

```

### 2. EDF (Earliest Deadline First) לללכ

כככלל ךל ךךל םלםכ לל לםםכ **כל לללל** לךכללכ. CPU םלכ 100%ךל םל ךכם לל לךכללכ.

```
 EDF לללכ ל 
                                             
  Task-A: לך=10ms, לםלך=4ms            
  Task-B: לך=20ms, לםלך=5ms            
  Task-C: לך=50ms, לםלך=10ms           
                                             
  לך >  0   4   8  10  14  20  24      
  לללל: B> A > C                        
  T-A:    [====]  [====]     [====]         
  T-B:         [====]      [====]          
  T-C:              [==========]            
                                             
  כככל ללכ כל לללל כך          
  CPU םלכ םך: U  1.0 (100%)            
  (כ, לכככ ל ככ םלם לם)          
                                             

```

### 3. RM vs EDF כך

> **כל:** RMל לך לךל לל לכל כל כלכ םכ ךללך, EDFכ כל לךל ךל ךךל לכל כל םלכ םכ ךללכ.

| םל | RM | EDF |
|------|----|----|
| **לללל** | לל (לך ךכ) | כל (כככל ךכ) |
| **CPU םלכ םך** | 69%(n->inf) | 100% |
| **ךם כלכ** | כל | כל (לללל כל כך) |
| **לכככ כל** | ללללל םלםכ לל | ככ םלם לם |
| **לל לל** | לל םל (POSIX ךכ) | לך + לכ ךם |

## . Linux PREEMPT_RT

### 1. ךל

PREEMPT_RT (Real-time Preemption) םלכ לכ Linux לכל ללך ללםלכ כםםכ םל לםלכ. לכ 5.x לם ללללכ כלכלל םםכך לכ.

```
 Linux Preemption Levels 
                                             
  PREEMPT_NONE:       לל כך              
  (לכ ךכ, לכ לככ)                   
                                             
  PREEMPT_VOLUNTARY:  ללל לל כך ל     
  (כלל לם םלם)                       
                                             
  PREEMPT_FULL:      לכ לככ לל ךכ   
  (כלםם ךכ, לםכם םככ לל)      
                                             
  PREEMPT_RT:        ךל ככ ך לל ךכ   
  (ללך, לםכםכ לככם)              
   לכ לכ לך כל                      
                                             

```

### 2. PREEMPT_RT לל כך לם

| כך | לכ | םך |
|------|------|------|
| **לםכם לככם** | םכ לםכםכ לכ לכככ כם | לםכם לל ללם |
| **לםכ כ לך** | כככל spinlockל mutexכ ךל | ללללל כל |
| **לללל לל** | כ ךל ל לללל לל לל | |
| **כלםל ךל** | לכ לכ לל ךכ לל םכ | לכככל לכ |

## . לל ךכם

```
ללך םכלל
 ללך ללם ככ
    םכ ללך (כככל לכ לל)
    לםם ללך (ךכ לכ םל)
    םל: לל ךכם לכ לך כל
 POSIX לללכ לל
    SCHED_FIFO (כל לללל FIFO)
    SCHED_RR (כל לללל Round Robin)
    SCHED_OTHER (CFS לכ םכלל)
    SCHED_DEADLINE (EDF ךכ לל)
 לללכ לךכל
    RM (Rate-Monotonic, לל, לך=לללל)
    EDF (Earliest Deadline First, כל)
    RM םך: U  n(2^(1/n)-1), EDF םך: U  1.0
 Linux PREEMPT_RT
    לכ לל לל: NONE < VOLUNTARY < FULL < RT
    לםכם לככם
    לםכ כל mutexכ ךל
    לללל לל כםל
 ללך ללם לךלם
    לכ לכ לך (Worst-case Latency) כל
    ךלל לם (Deterministic Execution)
    לם(Jitter) ללם
 לל כל
     םךלל לל ללם
     לללם לכל
     לל לכם (PLC)
     לכ ךך
```

---

## לל לכ

| לל | Full Name |
|------|-----------|
| **RTOS** | Real-Time Operating System |
| **RM** | Rate-Monotonic (Scheduling) |
| **EDF** | Earliest Deadline First |
| **PREEMPT_RT** | Real-Time Preemption Patch |
| **CFS** | Completely Fair Scheduler |
| **PLC** | Programmable Logic Controller |
| **ABS** | Anti-lock Braking System |

---

## 3ל לכל לכ

לםםך לםל לך לל ככל לל ככל םכ ללםלככ.
כםך לללכ לכל ככלםלכ כלכ לםם לל ללל.
ךל ללם לכם כל לכםך, לךל לככ ךכל לםם ללל םככ.
