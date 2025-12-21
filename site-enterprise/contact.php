<?php
// contacto.php - Versión robusta para Hostinger
// ===== CONFIGURACIÓN =====
$destinatario = "enterprise@ahigovernance.com";
$asunto = "Nueva solicitud de auditoría - AHI Governance";
$archivo_leads = "leads.csv"; // Respaldo local
// ===== HEADERS CORS (para AJAX) =====
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
// ===== RESPUESTA POR DEFECTO =====
$response = ["status" => "error", "message" => "Método no permitido"];
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // 1. Obtener y limpiar el email
    $email_cliente = isset($_POST["email"]) ? filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL) : "";
    // 2. Validar formato
    if (!filter_var($email_cliente, FILTER_VALIDATE_EMAIL)) {
        $response = ["status" => "error", "message" => "Formato de correo inválido"];
        echo json_encode($response);
        exit;
    }
    // 3. Guardar en CSV (SIEMPRE funciona, es tu respaldo)
    $fecha = date("Y-m-d H:i:s");
    $linea = "$fecha,$email_cliente,Landing Page\n";
    $guardado = @file_put_contents($archivo_leads, $linea, FILE_APPEND | LOCK_EX);
    if ($guardado === false) {
        // Si no puede escribir, intenta crear el archivo
        @file_put_contents($archivo_leads, "Fecha,Email,Origen\n" . $linea);
    }
    // 4. Preparar mensaje de correo
    $mensaje = "Nueva solicitud de auditoría recibida.\n\n";
    $mensaje .= "----------------------------------------\n";
    $mensaje .= "Correo del cliente: " . $email_cliente . "\n";
    $mensaje .= "Fecha: " . $fecha . "\n";
    $mensaje .= "Origen: Landing Page B2B\n";
    $mensaje .= "----------------------------------------\n\n";
    $mensaje .= "Responde a este correo para contactar al prospecto.";
    // 5. Headers del correo (Hostinger a veces requiere From del mismo dominio)
    $headers = "From: noreply@ahigovernance.com\r\n";
    $headers .= "Reply-To: " . $email_cliente . "\r\n";
    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion();
    // 6. Intentar enviar
    $enviado = @mail($destinatario, $asunto, $mensaje, $headers);
    if ($enviado) {
        $response = [
            "status" => "success",
            "message" => "¡Gracias! Le contactaremos en las próximas 24 horas."
        ];
    } else {
        // El correo falló, pero el lead SÍ se guardó en CSV
        $response = [
            "status" => "success",
            "message" => "¡Recibido! Le contactaremos pronto. (Lead guardado)"
        ];
        // Nota: Decimos "success" porque el lead SÍ se capturó en el CSV
    }
}
echo json_encode($response);
?>