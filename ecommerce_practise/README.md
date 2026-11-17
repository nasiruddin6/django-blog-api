# Ecommerce Practise — শেখার ছোট project

Original `../ecommerce`-এর একই structure ও function-based API রাখা হয়েছে। এখানে আলাদা SQLite database; original project-এর data copy করা হয়নি। একটি Brand, একটি Category, একটি Product, একটি Image, একটি Variant এবং একটি Attribute দিয়ে পুরো relation flow দেখবে। নতুন record বানানোর restriction নেই।

## Run

```bash
cd /home/nasir/projects_django/ecommerce_practise
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_practice
python manage.py runserver 8001
```

Swagger: http://127.0.0.1:8001/docs/ — প্রতিটি API expand করে **Try it out** দাও। Browsable API: http://127.0.0.1:8001/api/v1/brands/
Admin চাইলে `python manage.py createsuperuser`, তারপর `/admin/`। কোনো default admin/password নেই। `seed_practice` আবার run করলে existing sample edit overwrite করবে না; deleted sample ফিরিয়ে আনতে পারবে।

## Structure কীভাবে পড়বে

```text
manage.py
src/                         # settings, root urls, ASGI/WSGI
apps/products/
    models.py                # database fields ও relation
    serializers.py           # JSON conversion ও validation
    views.py                 # function-based GET/POST/PUT/PATCH/DELETE
    urls.py                  # endpoint → view
    admin.py                 # admin registration ও inline
    migrations/              # original schema history
    management/commands/seed_practice.py
    tests.py
```

Request flow: URL → view → serializer → model/database → JSON response। প্রথমে Brand-এর এই চারটি file পাশাপাশি পড়ো। সব API implemented আছে যেন working reference দেখে নিজে আবার লিখে মিলিয়ে নিতে পারো।

## Practice order

1. **Brand / basic CRUD:** `Brand` → `BrandSerializer` → `brand_list_create` → `brand_detail` → `urls.py` পড়ো। GET list/detail, POST, PUT, PATCH, DELETE করো। এরপর reference না দেখে একই flow লিখে আবার চালাও।
2. **Category / self relation:** Brand-এর pattern অনুসরণ করো। প্রথম sample-এর `parent=null`; আরেকটি Category বানিয়ে `parent`-এ প্রথমটির ID দাও। `parent_name` কেন read-only বুঝো।
3. **Product / ForeignKey:** Brand ও Category-এর response থেকে ID নিয়ে product বানাও। Response-এ writable `brand`/`category` ID এবং read-only `brand_name`/`category_name` দেখো। `select_related` কেন আছে দেখো।
4. **Attribute / one-to-many:** product ID দিয়ে `Material=Cotton` দেখো; আরেকটি attribute নিজে POST করো। Product detail-এর nested `attributes` check করো। Variant-ও একই pattern; SKU unique।
5. **Image / file upload:** `/product-images/`-এ multipart form দিয়ে `product` ID ও নিজের image file upload করো। Nested images read-only, তাই Product POST-এ images পাঠিয়ে save হবে না; আলাদা image endpoint ব্যবহার করো। `prefetch_related` কেন আছে দেখো।
6. **Validation / errors:** duplicate brand name ও SKU → 400, missing ID → 404, negative product price বা price-এর বেশি discount → 400। PATCH-এ শুধু price কমিয়েও existing discount conflict check করো। Product থাকা category delete → 400; brand delete করলে product-এর brand null হয়; product delete করলে related image/variant/attribute database rows delete হয়। Image file disk cleanup আলাদা বিষয়।
7. **নিজে extend করো:** Brand-এ `website` field যোগ → migration → serializer → Swagger POST/PATCH। এরপর Category-তে একই কাজ নিজে করো। Product list-এ `?status=published` filter নিজে যোগ করো; এখন filter implemented নেই।

## API map

প্রতিটি নিচের path-এর শুরু `/api/v1/`। List path-এ GET/POST; `<id>/`-এ GET/PUT/PATCH/DELETE।

| Model | List path | Detail path |
| --- | --- | --- |
| Brand | `brands/` | `brands/<id>/` |
| Category | `categories/` | `categories/<id>/` |
| Product | `products/` | `products/<id>/` |
| Image | `product-images/` | `product-images/<id>/` |
| Variant | `product-variants/` | `product-variants/<id>/` |
| Attribute | `product-attributes/` | `product-attributes/<id>/` |

## হাতে করে example

প্রথমে brands/categories GET করে আসল ID বসাও; ID সবসময় 1 হবে ধরে নিও না।

```json
{"name":"My T-Shirt","sku":"MY-002","brand":1,"category":1,"price":"600.00","stock":3}
```

উপরের JSON `/api/v1/products/`-এ POST করো। Returned product ID দিয়ে `/api/v1/product-attributes/`-এ:

```json
{"product":1,"name":"Color","value":"Blue"}
```

প্রথমে নিজের বোঝা যাচাই করো: `many=True` কেন? PATCH-এ `partial=True` কেন? slug কে বানায়? ForeignKey ID ও nested serializer-এর পার্থক্য কী? PUT-এ required fields আর PATCH-এ missing fields কীভাবে handle হয়?

## Checks ও feedback

```bash
python manage.py check
python manage.py test
python manage.py makemigrations --check --dry-run
```

Original-এর structure শেখার জন্য clear, related query optimization ও Swagger আছে। Practice version-এ product price/discount validation, protected category deletion-এর readable 400, image media URL এবং behaviour tests যোগ করা হয়েছে। Authentication/permissions, pagination, category cycle validation, variant price validation ও concurrency-safe slug generation future exercises; বর্তমান project local learning-এর জন্য। QuerySet practice list `querysets.txt`-এ আছে; প্রথমে basic/filter/relationship sections করো, পরে advanced sections।
