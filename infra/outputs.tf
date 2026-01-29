output "api_url" {
  description = "Public URL of the API"
  value       = "https://${azurerm_container_app.api.ingress[0].fqdn}"
}
