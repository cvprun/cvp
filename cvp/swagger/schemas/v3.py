# -*- coding: utf-8 -*-

import re
from typing import Any, Dict, List, Optional, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    RootModel,
    ValidationInfo,
    field_validator,
)


class SecurityRequirementObject(RootModel[Dict[str, List[str]]]):
    """
    A declaration of which security schemes are applied to the API or individual
    operations. The key is the name of a security scheme declared in
    ComponentsObject.securitySchemes. The value is a list of scope names required for
    the execution.
    """


class OAuthFlowObject(BaseModel):
    authorizationUrl: HttpUrl
    """
    The authorization URL to be used for this flow. This MUST be in the form of a URL.
    The OAuth2 standard requires the use of TLS.
    """

    tokenUrl: HttpUrl
    """
    The token URL to be used for this flow. This MUST be in the form of a URL.
    The OAuth2 standard requires the use of TLS.
    """

    scopes: Dict[str, str]
    """
    The available scopes for the OAuth2 security scheme. A map between the scope name
    and a short description for it. The map MAY be empty.
    """

    refreshUrl: Optional[HttpUrl] = None
    """
    The URL to be used for obtaining refresh tokens. This MUST be in the form of a URL.
    The OAuth2 standard requires the use of TLS.
    """


class OAuthFlowsObject(BaseModel):
    implicit: Optional[OAuthFlowObject] = None
    password: Optional[OAuthFlowObject] = None
    clientCredentials: Optional[OAuthFlowObject] = None
    authorizationCode: Optional[OAuthFlowObject] = None


class SecuritySchemeObject(BaseModel):
    type: str
    description: Optional[str] = None
    name: Optional[str] = None
    in_: Optional[str] = Field(None, alias="in")
    scheme: Optional[str] = None
    bearerFormat: Optional[str] = None
    flows: Optional[OAuthFlowsObject] = None
    openIdConnectUrl: Optional[HttpUrl] = None


class XMLObject(BaseModel):
    name: Optional[str] = None
    namespace: Optional[HttpUrl] = None
    prefix: Optional[str] = None
    attribute: Optional[bool] = False
    wrapped: Optional[bool] = False


class DiscriminatorObject(BaseModel):
    propertyName: str
    mapping: Optional[Dict[str, str]] = None


AdditionalPropertiesUnion = Union[bool, "SchemaObject", "ReferenceObject"]


class SchemaObject(BaseModel):
    """
    This is a simplified Schema Object.
    A full implementation would require a much more complex model due to its recursive
    nature and extensive JSON Schema support. For this task, we'll include common
    fields and allow for arbitrary additional properties.
    """

    title: Optional[str] = None
    multipleOf: Optional[float] = None
    maximum: Optional[float] = None
    exclusiveMaximum: Optional[bool] = False
    minimum: Optional[float] = None
    exclusiveMinimum: Optional[bool] = False
    maxLength: Optional[int] = Field(None, ge=0)
    minLength: Optional[int] = Field(0, ge=0)
    pattern: Optional[str] = None
    maxItems: Optional[int] = Field(None, ge=0)
    minItems: Optional[int] = Field(0, ge=0)
    uniqueItems: Optional[bool] = False
    maxProperties: Optional[int] = Field(None, ge=0)
    minProperties: Optional[int] = Field(0, ge=0)
    required: Optional[List[str]] = None
    enum: Optional[List[Any]] = None
    type: Optional[str] = None
    allOf: Optional[List[Union["SchemaObject", "ReferenceObject"]]] = None
    oneOf: Optional[List[Union["SchemaObject", "ReferenceObject"]]] = None
    anyOf: Optional[List[Union["SchemaObject", "ReferenceObject"]]] = None
    not_: Optional[Union["SchemaObject", "ReferenceObject"]] = Field(None, alias="not")
    items: Optional[Union["SchemaObject", "ReferenceObject"]] = None
    properties: Optional[Dict[str, Union["SchemaObject", "ReferenceObject"]]] = None
    additionalProperties: Optional[AdditionalPropertiesUnion] = None
    description: Optional[str] = None
    format: Optional[str] = None
    default: Optional[Any] = None
    nullable: Optional[bool] = False
    discriminator: Optional[DiscriminatorObject] = None
    readOnly: Optional[bool] = False
    writeOnly: Optional[bool] = False
    xml: Optional[XMLObject] = None
    externalDocs: Optional["ExternalDocumentationObject"] = None
    example: Optional[Any] = None
    deprecated: Optional[bool] = False


class ReferenceObject(BaseModel):
    ref: str = Field(alias="$ref")
    """
    The reference identifier. This MUST be in the form of a URI.
    """

    summary: Optional[str] = None
    """
    A short summary which by default SHOULD override that of the referenced component.
    If the referenced object-type does not allow a summary field,
    then this field has no effect.
    """

    description: Optional[str] = None
    """
    A description which by default SHOULD override that of the referenced component.
    CommonMark syntax MAY be used for rich text representation. If the referenced
    object-type does not allow a description field, then this field has no effect.
    """


class TagObject(BaseModel):
    name: str
    description: Optional[str] = None
    externalDocs: Optional["ExternalDocumentationObject"] = None


SchemaUnion = Union[SchemaObject, ReferenceObject]


class HeaderObject(BaseModel):
    description: Optional[str] = None
    required: Optional[bool] = False
    deprecated: Optional[bool] = False
    allowEmptyValue: Optional[bool] = False
    style: Optional[str] = None
    explode: Optional[bool] = None
    allowReserved: Optional[bool] = False
    schema_: Optional[SchemaUnion] = Field(None, alias="schema")
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union["ExampleObject", ReferenceObject]]] = None
    content: Optional[Dict[str, "MediaTypeObject"]] = None


class LinkObject(BaseModel):
    operationId: Optional[str] = None
    operationRef: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    requestBody: Optional[Any] = None
    description: Optional[str] = None
    server: Optional["ServerObject"] = None


class ExampleObject(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    value: Optional[Any] = None
    externalValue: Optional[HttpUrl] = None


class CallbackObject(RootModel[Dict[str, "PathItemObject"]]):
    """A map of a logical expression to a Path Item Object"""


class ResponseObject(BaseModel):
    description: str
    headers: Optional[Dict[str, Union[HeaderObject, ReferenceObject]]] = None
    content: Optional[Dict[str, "MediaTypeObject"]] = None
    links: Optional[Dict[str, Union[LinkObject, ReferenceObject]]] = None


class ResponsesObject(BaseModel):
    """
    A map of HTTP status codes to Response Objects.
    Can contain 'default' and HTTP status codes (like '200', '404', etc.)
    """

    model_config = ConfigDict(extra="allow")

    default: Optional[Union[ResponseObject, ReferenceObject]] = None
    """
    Default response for all HTTP status codes that are not covered by other responses
    """

    @staticmethod
    def _is_valid_status_code(code: Union[str, int]) -> bool:
        if isinstance(code, int):
            code = str(code)
        assert isinstance(code, str)

        if re.match(r"^[1-5]\d{2}$", code):
            return True
        elif re.match(r"^[1-5]XX$", code):
            return True

        return False

    # noinspection PyNestedDecorators
    @field_validator("*", mode="before")
    @classmethod
    def validate_response_fields(cls, v: Any, info: ValidationInfo):
        field_name = info.field_name

        if field_name.startswith("_") or field_name == "default":
            return v

        if not cls._is_valid_status_code(field_name):
            raise ValueError(
                f"Invalid response key: {field_name}."
                " Must be 'default' or valid HTTP status code"
            )

        return v

    def get_response(
        self,
        status_code: Union[str, int],
    ) -> Optional[Union[ResponseObject, ReferenceObject]]:
        if isinstance(status_code, int):
            status_code = str(status_code)
        assert isinstance(status_code, str)

        return getattr(self, status_code, None)

    def set_response(
        self,
        status_code: Union[str, int],
        response: Union[ResponseObject, ReferenceObject],
    ):
        if isinstance(status_code, int):
            status_code = str(status_code)
        assert isinstance(status_code, str)

        if not self._is_valid_status_code(status_code) and status_code != "default":
            raise ValueError(f"Invalid status code: {status_code}")

        setattr(self, status_code, response)


class EncodingObject(BaseModel):
    contentType: Optional[str] = None
    headers: Optional[Dict[str, Union[HeaderObject, ReferenceObject]]] = None
    style: Optional[str] = None
    explode: Optional[bool] = None
    allowReserved: Optional[bool] = False


class MediaTypeObject(BaseModel):
    schema_: Optional[SchemaUnion] = Field(None, alias="schema")
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[ExampleObject, ReferenceObject]]] = None
    encoding: Optional[Dict[str, EncodingObject]] = None


class RequestBodyObject(BaseModel):
    description: Optional[str] = None
    content: Dict[str, MediaTypeObject]
    required: Optional[bool] = False


class ParameterObject(BaseModel):
    name: str
    in_: str = Field(alias="in")  # Use alias for 'in' keyword
    description: Optional[str] = None
    required: Optional[bool] = False
    deprecated: Optional[bool] = False
    allowEmptyValue: Optional[bool] = False
    style: Optional[str] = None
    explode: Optional[bool] = None
    allowReserved: Optional[bool] = False
    schema_: Optional[SchemaUnion] = Field(None, alias="schema")
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[ExampleObject, ReferenceObject]]] = None
    content: Optional[Dict[str, MediaTypeObject]] = None


class ExternalDocumentationObject(BaseModel):
    description: Optional[str] = None
    url: HttpUrl


class OperationObject(BaseModel):
    tags: Optional[List[str]] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    externalDocs: Optional[ExternalDocumentationObject] = None
    operationId: Optional[str] = None
    parameters: Optional[List[Union[ParameterObject, ReferenceObject]]] = None
    requestBody: Optional[Union[RequestBodyObject, ReferenceObject]] = None
    responses: ResponsesObject
    callbacks: Optional[Dict[str, Union[CallbackObject, ReferenceObject]]] = None
    deprecated: Optional[bool] = False
    security: Optional[List[SecurityRequirementObject]] = None
    servers: Optional[List["ServerObject"]] = None


class PathItemObject(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    get: Optional[OperationObject] = None
    put: Optional[OperationObject] = None
    post: Optional[OperationObject] = None
    delete: Optional[OperationObject] = None
    options: Optional[OperationObject] = None
    head: Optional[OperationObject] = None
    patch: Optional[OperationObject] = None
    trace: Optional[OperationObject] = None
    servers: Optional[List["ServerObject"]] = None
    parameters: Optional[List[Union[ParameterObject, ReferenceObject]]] = None


class PathsObject(RootModel[Dict[str, PathItemObject]]):
    """
    This object is a map between a path and its Path Item Object.
    The keys are path templates, and the values are Path Item Objects.
    The specification uses a regex pattern for keys, which Pydantic doesn't directly
    support for field names.
    So, we'll use a generic Dict and rely on validation elsewhere if needed.
    """


SecuritySchemesDict = Dict[str, Union[SecuritySchemeObject, ReferenceObject]]


class ComponentsObject(BaseModel):
    schemas: Optional[Dict[str, Union[SchemaObject, ReferenceObject]]] = None
    responses: Optional[Dict[str, Union[ResponseObject, ReferenceObject]]] = None
    parameters: Optional[Dict[str, Union[ParameterObject, ReferenceObject]]] = None
    examples: Optional[Dict[str, Union[ExampleObject, ReferenceObject]]] = None
    requestBodies: Optional[Dict[str, Union[RequestBodyObject, ReferenceObject]]] = None
    headers: Optional[Dict[str, Union[HeaderObject, ReferenceObject]]] = None
    securitySchemes: Optional[SecuritySchemesDict] = None
    links: Optional[Dict[str, Union[LinkObject, ReferenceObject]]] = None
    callbacks: Optional[Dict[str, Union[CallbackObject, ReferenceObject]]] = None
    pathItems: Optional[Dict[str, Union[PathItemObject, ReferenceObject]]] = None


class ServerVariableObject(BaseModel):
    enum: Optional[List[str]] = None
    default: str
    description: Optional[str] = None


class ServerObject(BaseModel):
    url: HttpUrl
    description: Optional[str] = None
    variables: Optional[Dict[str, ServerVariableObject]] = None


class LicenseObject(BaseModel):
    name: str
    identifier: Optional[str] = None
    url: Optional[HttpUrl] = None


class ContactObject(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    email: Optional[str] = None


class InfoObject(BaseModel):
    title: str
    summary: Optional[str] = None
    description: Optional[str] = None
    termsOfService: Optional[HttpUrl] = None
    contact: Optional[ContactObject] = None
    license: Optional[LicenseObject] = None
    version: str


class OpenAPIObject(BaseModel):
    openapi: str
    info: InfoObject
    jsonSchemaDialect: Optional[HttpUrl] = None
    servers: Optional[List[ServerObject]] = None
    paths: Optional[PathsObject] = None
    webhooks: Optional[Dict[str, Union[PathItemObject, ReferenceObject]]] = None
    components: Optional[ComponentsObject] = None
    security: Optional[List[SecurityRequirementObject]] = None
    tags: Optional[List[TagObject]] = None
    externalDocs: Optional[ExternalDocumentationObject] = None


# Forward references for models that refer to each other
SecurityRequirementObject.model_rebuild()
OAuthFlowObject.model_rebuild()
OAuthFlowsObject.model_rebuild()
SecuritySchemeObject.model_rebuild()
XMLObject.model_rebuild()
DiscriminatorObject.model_rebuild()
SchemaObject.model_rebuild()
ReferenceObject.model_rebuild()
TagObject.model_rebuild()
HeaderObject.model_rebuild()
LinkObject.model_rebuild()
ExampleObject.model_rebuild()
CallbackObject.model_rebuild()
ResponseObject.model_rebuild()
ResponsesObject.model_rebuild()
EncodingObject.model_rebuild()
MediaTypeObject.model_rebuild()
RequestBodyObject.model_rebuild()
ParameterObject.model_rebuild()
ExternalDocumentationObject.model_rebuild()
OperationObject.model_rebuild()
PathItemObject.model_rebuild()
PathsObject.model_rebuild()
ComponentsObject.model_rebuild()
ServerVariableObject.model_rebuild()
ServerObject.model_rebuild()
LicenseObject.model_rebuild()
ContactObject.model_rebuild()
InfoObject.model_rebuild()
OpenAPIObject.model_rebuild()
