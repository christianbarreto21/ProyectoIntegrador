# 0004_crear_triggers.py
from django.db import migrations

def crear_trigger(apps, schema_editor):
    # Código SQL para crear el primer trigger
    sql_insert = """
    CREATE TRIGGER auditoria_evento_insert
    AFTER INSERT ON tareas_evento
    BEGIN
        INSERT INTO tareas_auditoriaevento (evento_id, operacion, descripcion)
        VALUES (NEW.id, 'INSERT', 'Se ha insertado un nuevo evento: ' || NEW.nombre);
    END;
    """
    schema_editor.execute(sql_insert)  # Ejecutar la primera sentencia

    # Código SQL para crear el segundo trigger
    sql_update = """
    CREATE TRIGGER auditoria_evento_update
    AFTER UPDATE ON tareas_evento
    BEGIN
        INSERT INTO tareas_auditoriaevento (evento_id, operacion, descripcion)
        VALUES (NEW.id, 'UPDATE', 'Se ha actualizado el evento: ' || NEW.nombre);
    END;
    """
    schema_editor.execute(sql_update)  # Ejecutar la segunda sentencia

def eliminar_trigger(apps, schema_editor):
    # Código SQL para eliminar los triggers si es necesario
    sql_drop_insert = """
    DROP TRIGGER IF EXISTS auditoria_evento_insert;
    """
    schema_editor.execute(sql_drop_insert)  # Eliminar el primer trigger

    sql_drop_update = """
    DROP TRIGGER IF EXISTS auditoria_evento_update;
    """
    schema_editor.execute(sql_drop_update)  # Eliminar el segundo trigger

class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0003_auditoriaevento'),
    ]

    operations = [
        migrations.RunPython(crear_trigger, eliminar_trigger),
    ]