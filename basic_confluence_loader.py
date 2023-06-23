from langchain.document_loaders import ConfluenceLoader

loader = ConfluenceLoader(
    url="https://confluence.internal.salesforce.com", username="yash.kulkarni", api_key="apiTokenAuthentication", confluence_kwargs={"verify_ssl": False}
)
documents = loader.load(space_key="CMEKB", include_attachments=True, limit=50)