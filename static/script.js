document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("empleado-form");
    const empleadosTable = document.getElementById("empleados-table");  // Asegúrate de que el ID coincida con tu tabla

    // Función para obtener todos los empleados
    async function obtenerEmpleados() {
        const response = await fetch("/api/empleados");
        const empleados = await response.json();

        empleadosTable.innerHTML = ""; // Limpiar la tabla

        empleados.forEach((empleado) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${empleado.nombre}</td>
                <td>${empleado.apellido}</td>
                <td>${empleado.email}</td>
                <td>${empleado.puesto}</td>
                <td>${empleado.salario}</td>
                <td>
                    <button class="eliminar" data-id="${empleado.id}">Eliminar</button>
                    <button class="editar" data-id="${empleado.id}">Editar</button>
                </td>
            `;
            empleadosTable.appendChild(row); // Agregar fila a la tabla
        });

        // Asignar eventos de edición y eliminación después de renderizar
        const editarButtons = document.querySelectorAll('.editar');
        const eliminarButtons = document.querySelectorAll('.eliminar');

        editarButtons.forEach(button => {
            button.addEventListener('click', () => {
                const id = button.getAttribute('data-id');
                editarEmpleado(id); // Llamar a la función editarEmpleado
            });
        });

        eliminarButtons.forEach(button => {
            button.addEventListener('click', () => {
                const id = button.getAttribute('data-id');
                eliminarEmpleado(id); // Llamar a la función eliminarEmpleado
            });
        });
    }

    // Evento para manejar el formulario
    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const id = document.getElementById("id").value;
        const nombre = document.getElementById("nombre").value;
        const apellido = document.getElementById("apellido").value;
        const email = document.getElementById("email").value;
        const puesto = document.getElementById("puesto").value;
        const salario = document.getElementById("salario").value;

        const method = id ? "PUT" : "POST";  // Determinar si es actualización o creación
        const url = id ? `/api/empleados/${id}` : "/api/empleados";  // URL de la API

        const response = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre, apellido, email, puesto, salario }),
        });

        if (response.ok) {
            form.reset();  // Limpiar el formulario
            obtenerEmpleados();  // Recargar la lista de empleados
        }
    });

    // Función para eliminar un empleado
    async function eliminarEmpleado(id) {
        const response = await fetch(`/api/empleados/${id}`, { method: "DELETE" });

        if (response.ok) obtenerEmpleados();  // Recargar la lista de empleados
    }

    // Función para editar un empleado
    async function editarEmpleado(id) {
        try {
            const response = await fetch(`/api/empleados/${id}`);
            
            if (!response.ok) {
                throw new Error('No se pudo obtener el empleado');
            }
            
            const empleado = await response.json();
    
            if (empleado && empleado.id) {
                document.getElementById("id").value = empleado.id;
                document.getElementById("nombre").value = empleado.nombre;
                document.getElementById("apellido").value = empleado.apellido;
                document.getElementById("email").value = empleado.email;
                document.getElementById("puesto").value = empleado.puesto;
                document.getElementById("salario").value = empleado.salario;
            } else {
                console.error("Empleado no encontrado");
            }
        } catch (error) {
            console.error("Error al editar el empleado:", error);
            alert("Ocurrió un error al intentar editar el empleado. Verifica la consola para más detalles.");
        }
    }
    
    
    

    // Llamada inicial para cargar los empleados
    obtenerEmpleados();
});
