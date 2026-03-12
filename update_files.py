import os
import re

directory = 'content/studynote/2_operating_system/3_cpu_scheduling/'
files = [f for f in os.listdir(directory) if f.endswith('.md') and f != '_index.md']

target_titles = {
    161: "161. 단기 스케줄러 (Short-term Scheduler) / CPU 스케줄러",
    162: "162. 중기 스케줄러 (Medium-term Scheduler) - 스와핑 (Swapping)",
    163: "163. 장기 스케줄러 (Long-term Scheduler) - 다중 프로그래밍 정도 조절",
    164: "164. I/O 바운드 프로세스 (I/O Bound Process)",
    165: "165. CPU 바운드 프로세스 (CPU Bound Process)",
    166: "166. 선점형 스케줄링 (Preemptive Scheduling)",
    167: "167. 비선점형 스케줄링 (Non-preemptive Scheduling)",
    168: "168. 디스패처 (Dispatcher) - 문맥 교환 수행 모듈",
    169: "169. 디스패치 지연 (Dispatch Latency)",
    170: "170. 스케줄링 기준 (Scheduling Criteria) - CPU 이용률, 처리량, 반환시간, 대기시간, 응답시간",
    171: "171. CPU 이용률 (CPU Utilization) / 처리량 (Throughput)",
    172: "172. 반환 시간 (Turnaround Time) / 대기 시간 (Waiting Time) / 응답 시간 (Response Time)",
    173: "173. FCFS (First-Come, First-Served) 스케줄링 - 비선점",
    174: "174. 호위 효과 (Convoy Effect) - FCFS의 단점",
    175: "175. SJF (Shortest Job First) 스케줄링 - 최적의 평균 대기 시간",
    176: "176. 지수 평균법 (Exponential Averaging) - 다음 CPU 버스트 길이 예측",
    177: "177. SRTF (Shortest Remaining Time First) 스케줄링 - SJF의 선점형 버전",
    178: "178. 라운드 로빈 (Round Robin, RR) 스케줄링 - 시분할 시스템, 선점형",
    179: "179. 시간 할당량 (Time Quantum / Time Slice) 의 크기와 문맥 교환 오버헤드",
    180: "180. 우선순위 스케줄링 (Priority Scheduling) - 무한 대기 문제 발생 가능",
    181: "181. 기아 상태 (Starvation / Indefinite Blocking)",
    182: "182. 노화 (Aging) - 기아 상태 해결책 (우선순위 점진적 상승)",
    183: "183. 다단계 큐 스케줄링 (Multilevel Queue Scheduling)",
    184: "184. 큐 간 스케줄링 (고정 우선순위 vs 시간 할당)",
    185: "185. 다단계 피드백 큐 스케줄링 (Multilevel Feedback Queue, MLFQ) - 프로세스의 큐 이동 허용",
    186: "186. MLFQ 파라미터 - 큐의 개수, 알고리즘, 승급/강등 기준",
    187: "187. HRN (Highest Response Ratio Next) 스케줄링 - (대기시간+서비스시간)/서비스시간",
    188: "188. 보장 스케줄링 (Guaranteed Scheduling)",
    189: "189. 복권 스케줄링 (Lottery Scheduling) - 확률적 스케줄링",
    190: "190. 공평 몫 스케줄링 (Fair-share Scheduling)",
    191: "191. 스레드 스케줄링 - 프로세스 경쟁 범위(PCS) vs 시스템 경쟁 범위(SCS)",
    192: "192. LWP 디스패치",
    193: "193. 다중 처리기 스케줄링 (Multiprocessor Scheduling)",
    194: "194. 비대칭 다중 처리 (ASMP) 스케줄링",
    195: "195. 대칭 다중 처리 (SMP) 스케줄링",
    196: "196. 부하 균등화 (Load Balancing) - Push Migration vs Pull Migration",
    197: "197. 프로세서 친화성 (Processor Affinity) - 캐시 최적화",
    198: "198. 멀티코어 스케줄링 (Multicore Scheduling) - 메모리 스톨 (Memory Stall) 대응",
    199: "199. 하이퍼스레딩 (Hyper-threading) / SMT (Simultaneous Multithreading) 스케줄링",
    200: "200. 이기종 다중 처리기 스케줄링 (HMP) - ARM big.LITTLE 구조",
    201: "201. 실시간 스케줄링 (Real-time Scheduling)",
    202: "202. 연성 실시간 (Soft Real-time) 시스템",
    203: "203. 경성 실시간 (Hard Real-time) 시스템",
    204: "204. 지연 시간 (Latency) - 인터럽트 지연 (Interrupt Latency) + 디스패치 지연 (Dispatch Latency)",
    205: "205. 주기적 태스크 (Periodic Task) - 주기(p), 마감시간(d), 실행시간(t)",
    206: "206. RM (Rate-Monotonic) 스케줄링 - 주기가 짧을수록 높은 우선순위 (정적 우선순위)",
    207: "207. EDF (Earliest Deadline First) 스케줄링 - 마감시간이 빠를수록 높은 우선순위 (동적 우선순위)",
    208: "208. 비례 배분 스케줄링 (Proportionate Share Scheduling)",
    209: "209. POSIX 스케줄링 API - SCHED_FIFO, SCHED_RR, SCHED_OTHER",
    210: "210. 리눅스 O(1) 스케줄러 - 두 개의 배열 (Active, Expired)",
    211: "211. 리눅스 CFS (Completely Fair Scheduler) - 가상 실행 시간 (vruntime) 기반, 레드-블랙 트리 사용",
    212: "212. 대상 지연 시간 (Target Latency) / 최소 입자 (Minimum Granularity)",
    213: "213. 윈도우 스케줄링 - 디스패처 (Dispatcher), 우선순위 기반 선점형, 32단계 우선순위",
    214: "214. 동적 우선순위 승급 (Priority Boost) - I/O 완료 시, GUI 전경 프로세스",
    215: "215. 태스크 스케줄링의 캐시 일관성 (Cache Coherence) 문제",
    216: "216. 에너지 인지 스케줄링 (Energy-Aware Scheduling, EAS)",
    217: "217. 코-스케줄링 (Co-scheduling / Gang Scheduling) - 밀접한 스레드 동시 스케줄링",
    218: "218. 컨테이너 스케줄링 (cgroups cpu.shares, cpu.cfs_quota_us)",
    219: "219. 실시간 리눅스 (PREEMPT_RT 패치)",
    220: "220. 무중단 라이브 마이그레이션 스케줄링 고려사항",
}

for filename in files:
    match = re.match(r'(\d+)_', filename)
    if match:
        weight = int(match.group(1))
        if weight in target_titles:
            new_title = target_titles[weight]
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update weight
            content = re.sub(r'^weight = \d+', f'weight = {weight}', content, flags=re.MULTILINE)
            # Update title
            content = re.sub(r'^title = ".*"', f'title = "{new_title}"', content, flags=re.MULTILINE)
            # Update h1 tag
            content = re.sub(r'^# .*', f'# {new_title[5:]}', content, flags=re.MULTILINE)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filename} with weight {weight} and title {new_title}")

missing = []
for i in range(161, 221):
    if not any(f.startswith(f"{i}_") for f in os.listdir(directory)):
        missing.append(i)

if missing:
    print("\nMissing keywords:")
    for m in missing:
        print(f"{m}. {target_titles[m]}")
