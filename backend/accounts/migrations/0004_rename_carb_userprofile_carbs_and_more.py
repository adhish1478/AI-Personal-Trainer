# Generated by Django 5.2.3 on 2025-06-28 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userprofile_height_alter_userprofile_weight'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='carb',
            new_name='carbs',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='fat',
            new_name='fats',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='goal',
            field=models.CharField(choices=[('lose_1kg', 'Lose 1 kg/week'), ('lose_0.75kg', 'Lose 0.75 kg/week'), ('lose_0.5kg', 'Lose 0.5 kg/week'), ('lose_0.25kg', 'Lose 0.25 kg/week'), ('maintain', 'Maintain weight'), ('lean_bulk', 'Lean bulk'), ('gain_0.25kg', 'Gain 0.25 kg/week'), ('gain_0.5kg', 'Gain 0.5 kg/week'), ('gain_0.75kg', 'Gain 0.75 kg/week'), ('gain_1kg', 'Gain 1 kg/week')], default='maintain', max_length=20),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lifts_weight',
            field=models.BooleanField(default=False),
        ),
    ]
