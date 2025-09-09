from apps.pages.models import ContactModel


def run():
    contacts = ContactModel.objects.all()
    print(contacts)


if __name__ == '__main__':
    run()
