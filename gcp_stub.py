"""Stub to mock user's consent store data. 

This saves us trouble for setting up Google cloud project with consent api.
In a real application, this stub should be replaced with a call to GCP API.
"""


def get_consent_store_context():
    return """
{
  "name": "projects/m6n3/locations/us-central1/datasets/test/consentStores/test-consent-store/consents/test-consent-id",
  "userId": "Sarah",
  "policies": [
    {
      "resourceAttributes": [
        {
          "attributeDefinitionId": "data_identifiable",
          "values": [
            "identifiable"
          ]
        }
      ],
      "authorizationRule": {
        "expression": "requester_identity == 'clinical-admin'"
      }
    },
    {
      "resourceAttributes": [
        {
          "attributeDefinitionId": "data_identifiable",
          "values": [
            "de-identified"
          ]
        }
      ],
      "authorizationRule": {
        "expression": "requester_identity in ['internal-researcher', 'external-researcher']"
      }
    }
  ],
  "consentArtifact": "projects/m6n3/locations/us-central1/datasets/test/consentStores/test-consent-store/consentArtifacts/test-consent-artifact-id",
  "state": "CONSENT_STATE",
  "stateChangeTime": "2023-01-01",
  "expireTime": "2026-01-01"
"""
