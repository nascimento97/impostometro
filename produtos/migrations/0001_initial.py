# Generated by Django 5.2.4 on 2025-07-19 12:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('despesafixa', '0001_initial'),
        ('despesavariavel', '0001_initial'),
        ('ingredientes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(help_text='Nome descritivo do produto', max_length=255, verbose_name='Nome do Produto')),
                ('descricao', models.TextField(blank=True, help_text='Descrição detalhada do produto', null=True, verbose_name='Descrição')),
                ('tempo_preparo', models.PositiveIntegerField(help_text='Tempo necessário para preparar o produto em minutos', verbose_name='Tempo de Preparo (minutos)')),
                ('margem_lucro', models.DecimalField(decimal_places=2, help_text='Margem de lucro desejada em percentual', max_digits=5, verbose_name='Margem de Lucro (%)')),
                ('periodo_analise', models.PositiveIntegerField(help_text='Período em dias para análise financeira', verbose_name='Período de Análise (dias)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('usuario', models.ForeignKey(help_text='Usuário proprietário do produto', on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'ordering': ['-created_at'],
                'unique_together': {('usuario', 'nome')},
            },
        ),
        migrations.CreateModel(
            name='ProdutoDespesaFixa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('despesa_fixa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produto_despesas_fixas', to='despesafixa.despesafixa', verbose_name='Despesa Fixa')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produto_despesas_fixas', to='produtos.produto', verbose_name='Produto')),
            ],
            options={
                'verbose_name': 'Produto Despesa Fixa',
                'verbose_name_plural': 'Produtos Despesas Fixas',
                'ordering': ['produto', 'despesa_fixa__nome'],
                'unique_together': {('produto', 'despesa_fixa')},
            },
        ),
        migrations.CreateModel(
            name='ProdutoDespesaVariavel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.DecimalField(decimal_places=3, help_text='Quantidade da despesa variável utilizada no produto', max_digits=10, verbose_name='Quantidade')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('despesa_variavel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produto_despesas_variaveis', to='despesavariavel.despesavariavel', verbose_name='Despesa Variável')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produto_despesas_variaveis', to='produtos.produto', verbose_name='Produto')),
            ],
            options={
                'verbose_name': 'Produto Despesa Variável',
                'verbose_name_plural': 'Produtos Despesas Variáveis',
                'ordering': ['produto', 'despesa_variavel__nome'],
                'unique_together': {('produto', 'despesa_variavel')},
            },
        ),
        migrations.CreateModel(
            name='ProdutoIngrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.DecimalField(decimal_places=3, help_text='Quantidade do ingrediente utilizada no produto', max_digits=10, verbose_name='Quantidade')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produto_ingredientes', to='ingredientes.ingrediente', verbose_name='Ingrediente')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produto_ingredientes', to='produtos.produto', verbose_name='Produto')),
            ],
            options={
                'verbose_name': 'Produto Ingrediente',
                'verbose_name_plural': 'Produtos Ingredientes',
                'ordering': ['produto', 'ingrediente__nome'],
                'unique_together': {('produto', 'ingrediente')},
            },
        ),
    ]
