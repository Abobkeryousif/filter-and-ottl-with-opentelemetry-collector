# OpenTelemetry Sensitive Traces Lab

معمل عملي من ثلاثة تطبيقات Python: `auth`, `payment`, و`flight`. كل تطبيق يولّد Traces تحتوي على بيانات تجريبية حساسة، ثم يرسلها إلى OpenTelemetry Collector حتى نجرّب `filter` و`transform` باستخدام OTTL.

> **تنبيه:** كل البيانات الواردة في المعمل وهمية ومخصصة للتجربة فقط. لا تستخدم بيانات عملاء أو بطاقات حقيقية.

## المكونات

- `auth`: تسجيل دخول وخصائص مثل البريد الإلكتروني واسم المستخدم وIP تجريبي.
- `payment`: معالجة دفع تجريبية مع رقم بطاقة وهمي ورقم طلب.
- `flight`: حجز رحلة تجريبي مع اسم مسافر ورقم جواز وهمي.
- `otel-collector`: يستقبل OTLP، يحذف بعض الـ spans المزعجة، ويخفي/يحذف الحقول الحساسة قبل التصدير إلى الـ debug exporter.

## التشغيل

من داخل هذا المجلد:

```bash
docker compose up --build
```

راقب سجلات الـ Collector:

```bash
docker compose logs -f otel-collector
```

سترى الـ spans التي اجتازت المعالجة. يفترض ألا تظهر القيم الحساسة الأصلية مثل البريد الإلكتروني أو رقم البطاقة أو رقم الجواز في الـ spans المصدّرة.

لإيقاف المعمل:

```bash
docker compose down
```

## أين نعدّل؟

- `otel-collector-config.yaml`: إعدادات `filter` و`transform` (OTTL).
- `app.py`: توليد الـ spans والـ attributes لكل تطبيق.
- `docker-compose.yml`: تشغيل التطبيقات الثلاثة والـ Collector.

## تجارب مقترحة

1. علّق سطر حذف `payment.card.number` داخل `transform`، شغّل المعمل مجدداً، ولاحظ كيف قد تتسرّب القيمة إلى الـ output.
2. غيّر شرط `filter` لتجاهل span آخر، مثل `auth.debug_noise`.
3. أضف attribute حساساً جديداً في أحد التطبيقات، ثم أضف له قاعدة masking أو حذف في `transform`.
4. قارن بين حذف span بالكامل عبر `filter` وبين حذف attribute واحد فقط عبر `transform`.

**مهم:** المعالجة داخل Collector طبقة دفاع إضافية وليست بديلاً عن تجنّب وضع الأسرار في telemetry من الأساس، أو عن ضوابط الحماية في التطبيق والـ backend.
