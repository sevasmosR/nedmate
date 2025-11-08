from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

FORM_RECOGNIZER_ENDPOINT = "https://novation.cognitiveservices.azure.com/"
FORM_RECOGNIZER_KEY = "22YhUPf7tHOIpLOxvSYZ0m6K0bOk8NCOqrrq6wXSCYJ2FShPl7j7JQQJ99BKACYeBjFXJ3w3AAALACOG0A1s"

client = DocumentAnalysisClient(
    endpoint=FORM_RECOGNIZER_ENDPOINT,
    credential=AzureKeyCredential(FORM_RECOGNIZER_KEY)
)

def safe_get_field(doc, field_name, default=None):
    """Safely get field value from Form Recognizer document."""
    field = doc.fields.get(field_name)
    if not field:
        return default

    # Handle CurrencyValue or Date types
    if hasattr(field.value, "amount"):
        return field.value.amount
    if hasattr(field.value, "to_date"):
        return field.value.to_date()
    return field.value

def parse_invoice(contents: bytes):
    """Parse invoice using Azure Form Recognizer prebuilt model."""
    poller = client.begin_analyze_document("prebuilt-invoice", contents)
    result = poller.result()

    invoice_data = {}
    if result.documents:
        doc = result.documents[0]
        invoice_data = {
            "merchant": safe_get_field(doc, "VendorName", "Unknown"),
            "total": safe_get_field(doc, "InvoiceTotal", 0.0),
            "invoice_date": safe_get_field(doc, "InvoiceDate"),
            "invoice_id": safe_get_field(doc, "InvoiceId"),
            "customer_name": safe_get_field(doc, "CustomerName"),
            "tax": safe_get_field(doc, "TotalTax", 0.0),
            "due_date": safe_get_field(doc, "DueDate"),
            "billing_address": safe_get_field(doc, "BillingAddress"),
            "shipping_address": safe_get_field(doc, "ShippingAddress"),
        }

    return invoice_data
