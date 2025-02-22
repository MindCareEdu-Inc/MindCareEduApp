from django.db import models
from django.core.validators import RegexValidator


class Administrador(models.Model):
    id_adm = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    contatos = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    sexo = models.CharField(max_length=20)
    senha = models.CharField(max_length=250)

# UF
class UF(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# City
class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    uf = models.ForeignKey(UF, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name


# Address
class Address(models.Model):
    id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=255)
    cep = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{5}-\d{3}$', 'Formato inválido de CEP. Exemplo: 12345-678')]
    )
    complement = models.CharField(max_length=255, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='addresses')
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['street', 'number', 'city', 'cep']  # Define que a combinação destes campos será única

    def __str__(self):
        return f"{self.street}, {self.number}, {self.city}"


# Organization
class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='organizations')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
# Server
class Server(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=255)  # Armazene como hash para segurança
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('staff', 'Staff')], default='staff')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='servers')
    active = models.BooleanField(default=True)
    reset_token = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.role}) - {self.organization.name}"


# Student
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')])
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=False)
    active = models.BooleanField(default=True)


    def _str_(self):
        return self.name


# Sentiment_History
class SentimentHistory(models.Model):
    id = models.AutoField(primary_key=True)
    result = models.CharField(max_length=100)
    confidence = models.DecimalField(max_digits=3, decimal_places=2)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='sentiment_history')
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.result} - {self.student.name}"

# Cadastro para login


class DadosAcademicos(models.Model):
    matricula = models.ForeignKey(Student, on_delete=models.CASCADE)
    curso = models.CharField(max_length=50)
    turma = models.CharField(max_length=100)
    notas = models.FloatField()
    media = models.FloatField()
    ira = models.FloatField()
    faltas = models.IntegerField()
    presenca = models.IntegerField()

class Emocoes(models.Model):
    id_emocao = models.AutoField(primary_key=True)
    matricula = models.ForeignKey(Student, on_delete=models.CASCADE)
    descricao = models.TextField()
    emocao_detectada = models.CharField(max_length=100)
    data_hora = models.DateTimeField()
    confianca = models.DecimalField(max_digits=5, decimal_places=2)
    foto = models.BinaryField()

class Relatorios(models.Model):
    id_relatorio = models.AutoField(primary_key=True)
    matricula = models.ForeignKey(Student, on_delete=models.CASCADE)
    id_emocao = models.ForeignKey(Emocoes, on_delete=models.CASCADE)
    emocao_detectada = models.CharField(max_length=100)
    relatorio = models.TextField()
    data_hora = models.DateTimeField()