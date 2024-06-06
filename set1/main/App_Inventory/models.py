from django.db import models
from django.utils import timezone
from django.core.files import File
from io import BytesIO
import qrcode


# Create your models here.

def upload_to(instance,filename):
    return 'images/{filename}'.format(filename=filename)


class CarInventory(models.Model):

    name = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    year = models.IntegerField()
    price = models.CharField(max_length=50)
    mileage = models.CharField(max_length=50)
    description = models.TextField()
    is_avaliable = models.BooleanField(default=True)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    QR_CODE = models.ImageField(upload_to='qrcodes',blank=False, null=False)
    created = models.DateTimeField(default=timezone.now().strftime('%Y-%m-%d-%H:%M:%S'))
    updated = models.DateTimeField(default=timezone.now().strftime('%Y-%m-%d-%H:%M:%S'))


    def save(self, *args, **kwargs):
        if not self.QR_CODE:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f'''

             Car Name : {self.name} \n
             Car Model : {self.model} \n
             Car Company : {self.company_name} \n
             Car Year : {self.year} \n
             Car Price : {self.price} \n
             Car Mileage : {self.mileage} \n
             Car Description : \t\t{self.description} \n 
             Car Is Avaliable : {self.is_avaliable} \n
             


            ''')
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            img.save(buffer, format='PNG')
            filename = f'qr_code_{self.name}.png'
            self.QR_CODE.save(filename, File(buffer),save=False)

        super(CarInventory,self).save(*args,**kwargs)
    
    def __str__(self):
        return self.name



