# Domain Suite Generator for Clean Architecture

This Cursor rule helps you quickly generate a complete domain suite for your clean architecture project. It creates all the necessary files for a new domain entity with proper structure and relationships.

## What it Creates

For each domain (e.g., Supplier, Ingredient), the rule generates:

1. **Domain Layer**
   - Domain model with base and full entity classes
   - Repository interface with CRUD methods

2. **Application Layer**
   - DTOs for create and update operations
   - Use cases implementing business logic

3. **Infrastructure Layer**
   - ORM model with SQLAlchemy mappings
   - SQL repository implementation

4. **API Layer**
   - REST endpoint with CRUD operations
   - Proper error handling and status codes

## How to Use

1. Open the Command Palette in Cursor (Ctrl+Shift+P or Cmd+Shift+P)
2. Type "Generate Domain Suite" and select the rule
3. Enter the domain name (e.g., "Supplier", "Ingredient")
4. The rule will generate all necessary files

## After Generation

After generating a new domain suite, you need to:

1. Update the router in `src/api/router.py` to include your new endpoint:
   ```python
   from api.endpoints import user_endpoint, your_domain_endpoint
   
   api_router = APIRouter()
   api_router.include_router(user_endpoint.router, prefix="/users", tags=["users"])
   api_router.include_router(your_domain_endpoint.router, prefix="/your_domains", tags=["your_domains"])
   ```

2. Customize the domain model with your specific fields in:
   - Domain model (`src/domain/models/your_domain.py`)
   - ORM model (`src/infrastructure/orm/your_domain_orm_model.py`)
   - Update the mapping methods in the ORM model

## Customization

You can customize the generated code by editing the rule file at `.cursor/rules/domain-suite-generator.js`. The rule uses template strings to generate the code, so you can modify the templates to match your project's specific needs. 