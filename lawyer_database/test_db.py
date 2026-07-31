from .crud import get_all_lawyers

lawyers = get_all_lawyers()

for lawyer in lawyers:

    print(dict(lawyer))