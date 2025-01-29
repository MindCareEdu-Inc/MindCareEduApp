from django.contrib import admin
from .models import Administrador, DadosAcademicos, Emocoes, Relatorios, UF, City, Address, Organization, Student, SentimentHistory

admin.site.register(Administrador)
admin.site.register(DadosAcademicos)
admin.site.register(Emocoes)
admin.site.register(Relatorios)
admin.site.register(UF)
admin.site.register(City)
admin.site.register(Address)
admin.site.register(Organization)
admin.site.register(Student)
admin.site.register(SentimentHistory)
