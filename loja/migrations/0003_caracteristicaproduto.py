from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0002_produto_vendido'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaracteristicaProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chave', models.CharField(max_length=100, verbose_name='Nome')),
                ('valor', models.CharField(max_length=200, verbose_name='Valor')),
                ('secao', models.CharField(
                    choices=[('principal', 'Características principais'), ('venda', 'Características de venda')],
                    default='principal',
                    max_length=20,
                    verbose_name='Seção',
                )),
                ('ordem', models.PositiveIntegerField(default=0, verbose_name='Ordem')),
                ('produto', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='caracteristicas',
                    to='loja.produto',
                    verbose_name='Produto',
                )),
            ],
            options={
                'verbose_name': 'Característica do Produto',
                'verbose_name_plural': 'Características do Produto',
                'ordering': ['secao', 'ordem', 'id'],
            },
        ),
    ]
