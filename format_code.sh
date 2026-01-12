#!/bin/bash

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Banner
echo ""
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}   🎨 Code Formatter & Linter 🎨      ${BLUE}║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    print_error "No se encuentra manage.py. Asegúrate de estar en la raíz del proyecto."
    exit 1
fi

print_success "Directorio del proyecto detectado"
echo ""

# Paso 1: Eliminar imports no usados
print_step "Paso 1/5: Eliminando imports y variables no usadas..."
if command -v autoflake &> /dev/null; then
    autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive . --exclude=venv
    print_success "Imports no usados eliminados"
else
    print_warning "autoflake no está instalado. Saltando este paso."
    echo "         Instalar con: pip install autoflake"
fi
echo ""

# Paso 2: Ordenar imports con isort
print_step "Paso 2/5: Ordenando imports con isort..."
if command -v isort &> /dev/null; then
    isort . --skip venv
    if [ $? -eq 0 ]; then
        print_success "Imports ordenados correctamente"
    else
        print_error "Error al ordenar imports"
        exit 1
    fi
else
    print_error "isort no está instalado. Instalar con: pip install isort"
    exit 1
fi
echo ""

# Paso 3: Formatear código con black
print_step "Paso 3/5: Formateando código con black..."
if command -v black &> /dev/null; then
    black . --exclude=venv
    if [ $? -eq 0 ]; then
        print_success "Código formateado correctamente"
    else
        print_error "Error al formatear código"
        exit 1
    fi
else
    print_error "black no está instalado. Instalar con: pip install black"
    exit 1
fi
echo ""

# Paso 4: Verificar con flake8
print_step "Paso 4/5: Verificando código con flake8..."
if command -v flake8 &> /dev/null; then
    flake8 . --exclude=venv,migrations
    if [ $? -eq 0 ]; then
        print_success "No se encontraron errores de linting"
    else
        print_warning "Se encontraron algunos problemas de linting (ver arriba)"
    fi
else
    print_warning "flake8 no está instalado. Saltando verificación."
    echo "         Instalar con: pip install flake8"
fi
echo ""

# Paso 5: Ejecutar tests (opcional)
print_step "Paso 5/5: ¿Ejecutar tests? (s/n)"
read -r run_tests

if [ "$run_tests" = "s" ] || [ "$run_tests" = "S" ]; then
    if command -v pytest &> /dev/null; then
        pytest -v
        if [ $? -eq 0 ]; then
            print_success "Todos los tests pasaron"
        else
            print_error "Algunos tests fallaron"
            exit 1
        fi
    else
        print_warning "pytest no está instalado"
    fi
else
    print_warning "Tests omitidos"
fi
echo ""

# Resumen
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}            🎉 COMPLETADO 🎉            ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""
print_success "El código está listo para commit"
echo ""
echo "Próximos pasos:"
echo "  1. git status              # Ver cambios"
echo "  2. git diff                # Revisar cambios"
echo "  3. git add .               # Agregar cambios"
echo "  4. git commit -m '...'     # Hacer commit"
echo "  5. git push origin main    # Subir a GitHub"
echo ""