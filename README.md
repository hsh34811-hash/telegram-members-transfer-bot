<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d0d0d,50:16213e,100:0f3460&height=220&section=header&text=telegram-members-transfer-bot&fontSize=36&fontColor=ffffff&fontAlignY=40&desc=✘%20𝙍𝘼𝙑𝙀𝙉%20|%20@P_X_24&descAlignY=62&descSize=20&animation=twinkling" />

<br/>

<a href="https://t.me/P_X_24">
  <img src="https://img.shields.io/badge/المطور-✘%20𝙍𝘼𝙑𝙀𝙉-0d0d0d?style=for-the-badge&logo=telegram&logoColor=white" />
</a>
<a href="https://t.me/P_X_24">
  <img src="https://img.shields.io/badge/Telegram-@P__X__24-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" />
</a>
<a href="https://www.python.org/">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</a>
<a href="https://docs.telethon.dev/">
  <img src="https://img.shields.io/badge/Telethon-Latest-0088cc?style=for-the-badge&logo=telegram&logoColor=white" />
</a>
<a href="LICENSE">
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge&logo=opensourceinitiative&logoColor=white" />
</a>

<br/><br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=2CA5E0&center=true&vCenter=true&width=700&lines=telegram-members-transfer-bot+%F0%9F%A4%96;Multi-Account+Members+Transfer;Join+%7C+Move+%7C+Check+%7C+Views;Built+by+%E2%9C%98+%F0%9D%99%8D%F0%9D%98%BC%F0%9D%99%91%F0%9D%99%80%F0%9D%99%89" />

</div>

---

<div dir="rtl">

## 🌐 اللغة | Language

**[العربية](#-نظرة-عامة)** &nbsp;|&nbsp; **[English](#-overview)**

---

## 📌 نظرة عامة

بوت تيليجرام متكامل لنقل الأعضاء بين المجموعات باستخدام حسابات متعددة، مع دعم المجموعات المقفولة وزيادة المشاهدات وفحص الحسابات — مبني بـ **Python** و **Telethon**.

---

## ✨ المميزات

| الميزة | الوصف |
|--------|-------|
| 👥 **نقل الأعضاء** | نقل الأعضاء بين المجموعات بشكل تلقائي |
| 🔓 **نقل متطور** | دعم المجموعات المقفولة (MovePro) |
| 📊 **فحص الحسابات** | فحص حالة جميع الحسابات المضافة |
| 👁️ **زيادة المشاهدات** | زيادة مشاهدات المنشورات |
| 🚪 **مغادرة المجموعات** | مغادرة المجموعات بالجملة |
| ⚡ **رشق الأعضاء** | ضخ الأعضاء لقنوات ومجموعات |
| 🔄 **متعدد الحسابات** | دعم حسابات متعددة في نفس الوقت |

---

## 📋 المتطلبات

- Python **3.10** أو أحدث
- حساب على [my.telegram.org](https://my.telegram.org) للحصول على `API_ID` و `API_HASH`
- بوتان من [@BotFather](https://t.me/BotFather)

---

## ⚙️ إعداد jello.ini

| المتغير | الوصف | المصدر |
|---------|-------|--------|
| `id` | معرف التطبيق | [my.telegram.org](https://my.telegram.org) |
| `hash` | هاش التطبيق | [my.telegram.org](https://my.telegram.org) |
| `adder` | معرف المشرف | Telegram User ID |
| `admin` | قائمة المشرفين | Telegram User IDs |
| `mover` | توكن البوت الأول | [@BotFather](https://t.me/BotFather) |
| `signer` | توكن البوت الثاني | [@BotFather](https://t.me/BotFather) |

---

## 🚀 طريقة التشغيل

**1. استنساخ المشروع**
```bash
git clone https://github.com/hsh34811-hash/telegram-members-transfer-bot.git
cd telegram-members-transfer-bot
```

**2. تثبيت المكتبات**
```bash
pip install -r requirements.txt
```

**3. إعداد الملف**
```bash
cp jello.ini.example jello.ini
# عدّل jello.ini وضع قيمك الحقيقية
```

**4. أضف ملفات الجلسات**
```bash
# ضع ملفات .session في مجلد sessions/
```

**5. تشغيل البوت**
```bash
python3 center.py
```

---

## 📱 الأوامر

| الأمر | الوصف |
|-------|-------|
| `/start` | عرض القائمة الرئيسية |
| `/copy` | بدء عملية نقل عادية |
| `/MovePro` | بدء نقل متطور للمجموعات المقفولة |
| `/check` | فحص حالة الحسابات |
| `/cancle` | إلغاء العملية الحالية |

---

## 🗂️ هيكل المشروع

```
📁 telegram-members-transfer-bot
├── 📄 center.py        # البوت الرئيسي
├── 📄 control.py       # التحكم في العمليات
├── 📄 bontrol.py       # نسخة بديلة للتحكم
├── 📄 database.py      # قاعدة البيانات
├── 📄 addAccount.py    # إضافة الحسابات
├── 📄 autoSigner.py    # التوقيع التلقائي
├── 📄 signerAccounts.py # إدارة الحسابات
├── 📄 texts.so         # النصوص
├── 📄 jello.ini        # ملف الإعدادات
├── 📁 sessions/        # ملفات الجلسات
├── 📁 database/        # ملفات قاعدة البيانات
└── 📄 README.md
```

---

## 👨‍💻 المطور

<div align="center">

| | |
|--|--|
| **الاسم** | ✘ 𝙍𝘼𝙑𝙀𝙉 |
| **تيليجرام** | [![Telegram](https://img.shields.io/badge/@P__X__24-2CA5E0?style=flat-square&logo=telegram&logoColor=white)](https://t.me/P_X_24) |

</div>

---

</div>

## 📌 Overview

A full-featured Telegram bot for transferring members between groups using multiple accounts, with support for locked groups, view boosting, and account checking — built with **Python** and **Telethon**.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 👥 **Member Transfer** | Auto transfer members between groups |
| 🔓 **Advanced Transfer** | Support for locked groups (MovePro) |
| 📊 **Account Check** | Check status of all added accounts |
| 👁️ **View Boosting** | Boost post views |
| 🚪 **Leave Groups** | Mass leave groups |
| ⚡ **Member Injection** | Inject members into channels/groups |
| 🔄 **Multi-Account** | Support multiple accounts simultaneously |

---

## 📋 Requirements

- Python **3.10** or newer
- Account on [my.telegram.org](https://my.telegram.org) for `API_ID` & `API_HASH`
- Two bots from [@BotFather](https://t.me/BotFather)

---

## 🚀 Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/hsh34811-hash/telegram-members-transfer-bot.git
cd telegram-members-transfer-bot
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Setup config**
```bash
cp jello.ini.example jello.ini
# Edit jello.ini and fill in your values
```

**4. Add session files**
```bash
# Place .session files in sessions/ folder
```

**5. Run the bot**
```bash
python3 center.py
```

---

## 👨‍💻 Developer

<div align="center">

| | |
|--|--|
| **Name** | ✘ 𝙍𝘼𝙑𝙀𝙉 |
| **Telegram** | [![Telegram](https://img.shields.io/badge/@P__X__24-2CA5E0?style=flat-square&logo=telegram&logoColor=white)](https://t.me/P_X_24) |

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f3460,50:16213e,100:0d0d0d&height=130&section=footer&animation=twinkling" />

**Made with ❤️ by [✘ 𝙍𝘼𝙑𝙀𝙉](https://t.me/P_X_24)**

</div>
