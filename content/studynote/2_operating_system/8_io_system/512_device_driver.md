+++
title = "512. 장치 드라이버"
weight = 512
+++

# 512. 장치 드라이버 (Device Driver)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 하드웨어와 OS 간 인터페이스 소프트웨어
> 2. **가치**: 하드웨어 추상화와 이식성
> 3. **융합**: 모듈, 인터럽트, 파일 시스템과 연관

---

## Ⅰ. 개요

### 개념 정의

장치 드라이버(Device Driver)는 **운영체제와 하드웨어 장치 사이의 통신을 담당하는 소프트웨어**이다.

### 💡 비유: 통역사
장치 드라이버는 **통역사**와 같다. OS의 요청을 하드웨어가 이해하는 언어로 번역한다.

### 장치 드라이버 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                장치 드라이버 구조                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【계층 구조】                                                          │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────┐    │ │
│  │  │              사용자 응용 프로그램                          │    │ │
│  │  │              open(), read(), write(), close()             │    │ │
│  │  └─────────────────────────────────────────────────────────┘    │ │
│  │                          │                                       │ │
│  │                          ▼                                       │ │
│  │  ┌─────────────────────────────────────────────────────────┐    │ │
│  │  │              VFS (Virtual File System)                    │    │ │
│  │  │              파일 디스크립터, inode                        │    │ │
│  │  └─────────────────────────────────────────────────────────┘    │ │
│  │                          │                                       │ │
│  │                          ▼                                       │ │
│  │  ┌─────────────────────────────────────────────────────────┐    │ │
│  │  │              장치 드라이버                                 │    │ │
│  │  │  ┌─────────────────────────────────────────────────────┐ │    │ │
│  │  │  │  file_operations                                     │ │    │ │
│  │  │  │  • open, release                                     │ │    │ │
│  │  │  │  • read, write                                       │ │    │ │
│  │  │  │  • ioctl, mmap                                       │ │    │ │
│  │  │  └─────────────────────────────────────────────────────┘ │    │ │
│  │  └─────────────────────────────────────────────────────────┘    │ │
│  │                          │                                       │ │
│  │                          ▼                                       │ │
│  │  ┌─────────────────────────────────────────────────────────┐    │ │
│  │  │              I/O 컨트롤러 (하드웨어)                        │    │ │
│  │  └─────────────────────────────────────────────────────────┘    │ │
│  │                          │                                       │ │
│  │                          ▼                                       │ │
│  │  ┌─────────────────────────────────────────────────────────┐    │ │
│  │  │              물리적 장치                                   │    │ │
│  │  └─────────────────────────────────────────────────────────┘    │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【드라이버 분류】                                                        │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  분류             설명                    예시                              │ │
│  │  ────             ────                    ────                              │ │
│  │  블록 드라이버     블록 단위 접근           디스크, SSD                      │ │
│  │  캐릭터 드라이버   바이트 스트림 접근        키보드, 마우스, 시리얼           │ │
│  │  네트워크 드라이버 패킷 단위 전송           NIC                             │ │
│  │  MISC 드라이버    기타 장치                /dev/random, /dev/null         │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석

### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                장치 드라이버 상세                                       │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【Linux 커널 모듈】                                                     │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  // 모듈 초기화/해제                                                     │ │
│  │  module_init(my_init);                                                  │ │
│  │  module_exit(my_exit);                                                  │ │
│  │  MODULE_LICENSE("GPL");                                                 │ │
│  │  MODULE_AUTHOR("Author");                                               │ │
│  │  MODULE_DESCRIPTION("Driver Description");                              │ │
│  │                                                             │ │
│  │  // file_operations 구조체                                               │ │
│  │  struct file_operations {                                               │ │
│  │      struct module *owner;                                              │ │
│  │      loff_t (*llseek)(struct file *, loff_t, int);                      │ │
│  │      ssize_t (*read)(struct file *, char __user *, size_t, loff_t *);   │ │
│  │      ssize_t (*write)(struct file *, const char __user *, size_t, ...); │ │
│  │      int (*open)(struct inode *, struct file *);                        │ │
│  │      int (*release)(struct inode *, struct file *);                     │ │
│  │      long (*unlocked_ioctl)(struct file *, unsigned int, unsigned long);│ │
│  │      int (*mmap)(struct file *, struct vm_area_struct *);               │ │
│  │  };                                                                     │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【문자 디바이스 등록】                                                  │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  1. dev_t 할당: alloc_chrdev_region()                                    │ │
│  │  2. cdev 초기화: cdev_init()                                             │ │
│  │  3. cdev 추가: cdev_add()                                                │ │
│  │  4. 장치 노드 생성: mknod /dev/mydev c MAJOR MINOR                       │ │
│  │  5. 클래스 생성: class_create()                                          │ │
│  │  6. 장치 생성: device_create()                                           │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【주요 API】                                                            │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  기능                  함수                                                │ │
│  │  ────                  ────                                                │ │
│  │  메모리 할당           kmalloc, kfree, devm_kmalloc                      │ │
│  │  사용자 공간 복사       copy_to_user, copy_from_user                      │ │
│  │  I/O 메모리 매핑       ioremap, iounmap                                   │ │
│  │  I/O 포트 접근         inb, outb, readb, writeb                           │ │
│  │  인터럽트 등록         request_irq, free_irq                              │ │
│  │  DMA                  dma_alloc_coherent, dma_map_single                  │ │
│  │  대기 큐              wait_queue, wait_event                             │ │
│  │  뮤텍스              mutex_lock, mutex_unlock                            │ │
│  │  스핀락              spin_lock, spin_unlock                              │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 실무 적용

### 구현 예시
```
┌─────────────────────────────────────────────────────────────────────┐
│                실무 적용                                            │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【드라이버 정보 확인】                                                  │
│  ──────────────────                                                  │
│  // 로드된 모듈 목록                                                    │
│  $ lsmod                                                             │
│  Module              Size  Used by                                   │
│  nvidia           12345678  0                                        │
│  snd_hda_intel      45056  0                                         │
│                                                                     │
│  // 모듈 상세 정보                                                      │
│  $ modinfo <module_name>                                             │
│  $ modinfo e1000e                                                    │
│                                                                     │
│  // 장치 정보                                                          │
│  $ lspci -k                                                          │
│  $ lsusb -v                                                          │
│  $ cat /proc/devices                                                 │
│                                                                     │
│  【모듈 로드/언로드】                                                    │
│  ──────────────────                                                  │
│  // 모듈 로드                                                          │
│  $ sudo insmod mydriver.ko                                           │
│  $ sudo modprobe mydriver                                            │
│                                                                     │
│  // 모듈 언로드                                                        │
│  $ sudo rmmod mydriver                                               │
│  $ sudo modprobe -r mydriver                                         │
│                                                                     │
│  // 의존성 확인                                                        │
│  $ modprobe --show-depends mydriver                                  │
│  $ depmod -a                                                         │
│                                                                     │
│  【간단한 문자 디바이스 드라이버】                                       │
│  ──────────────────                                                  │
│  #include <linux/module.h>                                           │
│  #include <linux/fs.h>                                               │
│  #include <linux/cdev.h>                                             │
│  #include <linux/uaccess.h>                                          │
│                                                                     │
│  #define DEVICE_NAME "mydev"                                         │
│  #define BUF_LEN 1024                                                │
│                                                                     │
│  static int major;                                                   │
│  static char msg[BUF_LEN];                                           │
│  static struct class *my_class;                                      │
│  static struct device *my_device;                                    │
│                                                                     │
│  static int my_open(struct inode *inode, struct file *file) {        │
│      return 0;                                                        │
│  }                                                                   │
│                                                                     │
│  static int my_release(struct inode *inode, struct file *file) {     │
│      return 0;                                                        │
│  }                                                                   │
│                                                                     │
│  static ssize_t my_read(struct file *file, char __user *buf,         │
│                          size_t count, loff_t *ppos) {               │
│      return copy_to_user(buf, msg, count) ? -EFAULT : count;          │
│  }                                                                   │
│                                                                     │
│  static ssize_t my_write(struct file *file, const char __user *buf,  │
│                           size_t count, loff_t *ppos) {              │
│      return copy_from_user(msg, buf, count) ? -EFAULT : count;        │
│  }                                                                   │
│                                                                     │
│  static struct file_operations fops = {                              │
│      .owner = THIS_MODULE,                                           │
│      .open = my_open,                                                │
│      .release = my_release,                                          │
│      .read = my_read,                                                │
│      .write = my_write,                                              │
│  };                                                                  │
│                                                                     │
│  static int __init my_init(void) {                                   │
│      major = register_chrdev(0, DEVICE_NAME, &fops);                 │
│      if (major < 0) return major;                                    │
│                                                                     │
│      my_class = class_create(THIS_MODULE, DEVICE_NAME);              │
│      my_device = device_create(my_class, NULL, MKDEV(major, 0),      │
│                                NULL, DEVICE_NAME);                   │
│      return 0;                                                        │
│  }                                                                   │
│                                                                     │
│  static void __exit my_exit(void) {                                  │
│      device_destroy(my_class, MKDEV(major, 0));                      │
│      class_destroy(my_class);                                        │
│      unregister_chrdev(major, DEVICE_NAME);                          │
│  }                                                                   │
│                                                                     │
│  module_init(my_init);                                               │
│  module_exit(my_exit);                                               │
│  MODULE_LICENSE("GPL");                                              │
│                                                                     │
│  【ioctl 구현】                                                        │
│  ──────────────────                                                  │
│  #define MY_IOCTL_CMD _IOR('M', 1, int)                              │
│                                                                     │
│  static long my_ioctl(struct file *file, unsigned int cmd,           │
│                       unsigned long arg) {                           │
│      switch (cmd) {                                                  │
│      case MY_IOCTL_CMD:                                              │
│          // 명령 처리                                                  │
│          break;                                                       │
│      default:                                                         │
│          return -EINVAL;                                              │
│      }                                                               │
│      return 0;                                                        │
│  }                                                                   │
│                                                                     │
│  // Makefile                                                          │
│  obj-m += mydriver.o                                                 │
│  all:                                                                │
│      make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules   │
│  clean:                                                              │
│      make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean     │
│                                                                     │
│  【드라이버 디버깅】                                                    │
│  ──────────────────                                                  │
│  // dmesg로 로그 확인                                                  │
│  $ dmesg | tail -20                                                  │
│  $ dmesg -w   // 실시간 모니터링                                        │
│                                                                     │
│  // ftrace로 추적                                                      │
│  $ echo function > /sys/kernel/debug/tracing/current_tracer         │
│  $ echo my_* > /sys/kernel/debug/tracing/set_ftrace_filter          │
│  $ echo 1 > /sys/kernel/debug/tracing/tracing_on                    │
│  $ cat /sys/kernel/debug/tracing/trace                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론

### 핵심 요약

```
• 개념: OS와 하드웨어 간 인터페이스 소프트웨어
• 분류: 블록, 캐릭터, 네트워크, MISC
• 구조: file_operations 인터페이스
• 등록: register_chrdev, cdev_add
• API: kmalloc, copy_to_user, ioremap
• 모듈: insmod, rmmod, modprobe
• 확인: lsmod, modinfo, lspci -k
• 디버깅: dmesg, ftrace, /sys/kernel/debug
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [I/O 컨트롤러](./503_io_controller.md) → 하드웨어 인터페이스
- [인터럽트 핸들러](./508_interrupt_handler.md) → 이벤트 처리
- [VFS](../9_file_system/476_vfs.md) → 파일 인터페이스

### 👶 어린이를 위한 3줄 비유 설명

**개념**: 장치 드라이버는 "통역사" 같아요!

**원리**: 서로 다른 언어를 연결해요!

**효과**: 하드웨어를 쓸 수 있어요!
