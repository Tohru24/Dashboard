"""Init

Revision ID: 50016d57bae4
Revises: 
Create Date: 2023-01-10 15:03:18.954694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50016d57bae4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dia', sa.String(length=15), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('dia')
    )
    op.create_table('productos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=60), nullable=False),
    sa.Column('categoria', sa.Enum('organico', 'inorganico', name='productcategory'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('role', sa.Enum('master', 'distribuidor', name='roletype'), nullable=False),
    sa.Column('status', sa.Enum('activo', 'inactivo', name='userstatus'), server_default='activo', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('copia_disponibilidades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('producto', sa.String(length=60), nullable=False),
    sa.Column('categoria', sa.String(length=60), nullable=False),
    sa.Column('cantidad', sa.Float(), nullable=False),
    sa.Column('unidad', sa.Enum('kg', 'lb', name='productmeasurement'), nullable=False),
    sa.Column('status', sa.Enum('sin_modificar', 'modificado', name='productstatus'), server_default='sin_modificar', nullable=False),
    sa.Column('fecha_de_creacion', sa.Date(), nullable=False),
    sa.Column('fecha_de_modificacion', sa.Date(), nullable=False),
    sa.Column('fecha_de_disponibilidad', sa.Date(), nullable=False),
    sa.Column('dia_de_disponibilidad', sa.Enum('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo', name='dias_de_disponibilidad'), nullable=False),
    sa.Column('creador_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creador_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('disp_dias_de_distribuidores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dia', sa.Integer(), nullable=False),
    sa.Column('usuario', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dia'], ['dias.id'], ),
    sa.ForeignKeyConstraint(['usuario'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('disp_usuario_productos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('producto', sa.Integer(), nullable=False),
    sa.Column('usuario', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['producto'], ['productos.id'], ),
    sa.ForeignKeyConstraint(['usuario'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('disponibilidades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('producto', sa.String(length=60), nullable=False),
    sa.Column('categoria', sa.String(length=60), nullable=False),
    sa.Column('cantidad', sa.Float(), nullable=False),
    sa.Column('unidad', sa.Enum('kg', 'lb', name='productmeasurement'), nullable=False),
    sa.Column('status', sa.Enum('sin_modificar', 'modificado', name='productstatus'), server_default='sin_modificar', nullable=False),
    sa.Column('fecha_de_creacion', sa.Date(), nullable=False),
    sa.Column('fecha_de_modificacion', sa.Date(), nullable=False),
    sa.Column('fecha_de_disponibilidad', sa.Date(), nullable=False),
    sa.Column('dia_de_disponibilidad', sa.Enum('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo', name='dias_de_disponibilidad'), nullable=False),
    sa.Column('modificador_id', sa.Integer(), nullable=False),
    sa.Column('creador_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creador_id'], ['usuarios.id'], ),
    sa.ForeignKeyConstraint(['modificador_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('log_disponibilidades',
    sa.Column('producto', sa.String(length=60), nullable=False),
    sa.Column('categoria', sa.String(length=60), nullable=False),
    sa.Column('cantidad', sa.Float(), nullable=False),
    sa.Column('unidad', sa.Enum('kg', 'lb', name='productmeasurement'), nullable=False),
    sa.Column('status', sa.Enum('sin_modificar', 'modificado', name='productstatus'), nullable=False),
    sa.Column('fecha_de_creacion', sa.Date(), nullable=False),
    sa.Column('fecha_de_modificacion', sa.Date(), nullable=False),
    sa.Column('fecha_de_disponibilidad', sa.Date(), nullable=False),
    sa.Column('dia_de_disponibilidad', sa.String(length=30), nullable=False),
    sa.Column('modificador_id', sa.Integer(), nullable=False),
    sa.Column('disponibilidad_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['disponibilidad_id'], ['disponibilidades.id'], ),
    sa.ForeignKeyConstraint(['modificador_id'], ['usuarios.id'], )
    )

    op.execute('''
                        CREATE OR REPLACE FUNCTION log_function()
                        RETURNS TRIGGER AS $$
                        begin 

                        NEW.fecha_de_modificacion := (now() AT TIME ZONE 'America/Bogota');


                        insert into "log_disponibilidades" values (old.producto, old.categoria, old.cantidad, old.unidad, old.status, old.fecha_de_creacion, new.fecha_de_modificacion, old.fecha_de_disponibilidad, old.dia_de_disponibilidad, old.modificador_id, old.id);

                        return new;
                        end;
                        $$
                        LANGUAGE plpgsql;
                        ''')
    op.execute('''
                            CREATE TRIGGER log_trigger
                            BEFORE UPDATE ON disponibilidades
                            FOR EACH ROW
                            EXECUTE FUNCTION log_function();
                            '''
               )

    op.execute('''
                    CREATE OR REPLACE FUNCTION insert_into_copia()
                    RETURNS TRIGGER AS $$
                    BEGIN
                        INSERT INTO copia_disponibilidades (id, producto, categoria, cantidad, unidad, status, fecha_de_creacion, fecha_de_modificacion, fecha_de_disponibilidad, dia_de_disponibilidad, creador_id) 
                        VALUES (NEW.id, NEW.producto, NEW.categoria, NEW.cantidad, NEW.unidad, NEW.status, NEW.fecha_de_creacion, NEW.fecha_de_modificacion, NEW.fecha_de_disponibilidad, NEW.dia_de_disponibilidad, NEW.creador_id);
                        RETURN NEW;
                    END;
                    $$
                    LANGUAGE plpgsql;
                    ''')
    op.execute('''
                        CREATE TRIGGER insert_into_copia_trigger
                        BEFORE INSERT ON disponibilidades
                        FOR EACH ROW
                        EXECUTE FUNCTION insert_into_copia();
                        '''
               )

    op.execute('''
                        CREATE OR REPLACE FUNCTION update_into_copia()
                        RETURNS TRIGGER AS $$
                        BEGIN
                            UPDATE copia_disponibilidades
                            SET producto = NEW.producto,
                                categoria = NEW.categoria,
                                cantidad = NEW.cantidad,
                                unidad = NEW.unidad,
                                status = NEW.status,
                                fecha_de_creacion = NEW.fecha_de_creacion,
                                fecha_de_modificacion = NEW.fecha_de_modificacion,
                                fecha_de_disponibilidad = NEW.fecha_de_disponibilidad,
                                dia_de_disponibilidad = NEW.dia_de_disponibilidad,
                                creador_id = NEW.creador_id
                            WHERE copia_disponibilidades.id = NEW.id;
                            RETURN NEW;
                        END;
                        $$
                        LANGUAGE plpgsql;
                        ''')
    op.execute('''
                            CREATE TRIGGER update_into_copia_trigger
                            AFTER UPDATE ON disponibilidades
                            FOR EACH ROW
                            EXECUTE FUNCTION update_into_copia();
                            '''
               )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('log_disponibilidades')
    op.drop_table('disponibilidades')
    op.drop_table('disp_usuario_productos')
    op.drop_table('disp_dias_de_distribuidores')
    op.drop_table('copia_disponibilidades')
    op.drop_table('usuarios')
    op.drop_table('productos')
    op.drop_table('dias')
    op.execute('DROP TRIGGER log_trigger ON disponibilidades')
    op.execute('DROP TRIGGER insert_into_copia_trigger ON disponibilidades')
    op.execute('DROP TRIGGER update_into_copia_trigger ON disponibilidades')
    op.execute('DROP FUNCTION log_function')
    op.execute('DROP FUNCTION insert_into_copia')
    op.execute('DROP FUNCTION update_into_copia')
    # ### end Alembic commands ###