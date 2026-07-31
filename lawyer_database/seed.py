from .crud import add_lawyer

lawyers = [

(
"Adv. Shanaya",
"shanaya@gmail.com",
"6466523710",
"Manhattan, NYC",
"NYC17264",
"New York",
10,
"Rental Law",
"uploads/bar_council_ids/shanaya.pdf",
"uploads/certificates/shanaya.pdf"
),

(
"Adv. Tim Grey",
"tim@gmail.com",
"7186533711",
" albany, nyc",
"NYC98194",
"New York",
12,
"Criminal Law",
"uploads/bar_council_ids/tim_greyt.pdf",
"uploads/certificates/tim_grey.pdf"
)

]

for lawyer in lawyers:

    add_lawyer(*lawyer)

print("Sample lawyers inserted.")