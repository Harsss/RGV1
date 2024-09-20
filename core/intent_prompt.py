
from kor.nodes import Object, Text

intents = Object(
    id="user_intents",
    description="You are chatmro, an MRO industry e-commerce chatbot. The intent of the user in the query and the entities involved. Identify the user's intent and extract relevant entities.",
    attributes=[
        Text(id="intent", description=
             '''
             User intent in the query. Intents should only be classified in one of the following intents and lowercase as well.
             **Intents:**
                1) buy - Intent if the user wants to buy a product
                2) specifications request/question - Intent if the user wants to know the specs of a product
                3) price request - Intent if the user wants to know the price, quote, RFQ (request for quote) of a product
                4) lead time request - Intent if the user wants to know the lead time of a product
                5) availability - Intent if the user wants to know the availability of a product
                6) letter request - Intent if the user requests a letter related to a product (e.g., compliance letter)
                7) certifications / standards - Intent if the user wants to know the standard approval and certificates of a product
                8) alternate product/s request - Intent if the user wants to know the alternates or spares of a product
                9) cheaper alternative request - Intent if someone asks for an alternative which is cheaper
                10) better lead time request - Intent if someone asks for a product with a better lead time
                11) brand alternate request - Intent if the user wants an alternative product from a different brand
                12) spare request - Intent if the user requests spare parts for a product
                13) kit request - Intent if the user requests a kit related to a product
                14) accessories request - Intent if the user requests accessories related to a product
                15) use - Intent if the user wants to know the use cases and uses of a product
                16) install - Intent if the user wants to know the installation process of a product
                17) repair - Intent if the user wants to know the repair process of a product
                18) use (category) - Intent if the user wants to know the use cases for a product category
                19) install (category) - Intent if the user wants to know the installation process for a product category
                20) repair (category) - Intent if the user wants to know the repair process for a product category
                21) use (category+specs) - Intent if the user wants to know the working mechanism of a product given its specs and category
                22) install (category+specs) - Intent if the user wants to know the installation process of a product given its specs and category
                23) repair (category+specs) - Intent if the user wants to know the repair process of a product given its specs and category
                24) requirement to category - Intent if the user has a requirement and wants to know the product category
                25) category to subcategory/product - Intent if the user knows the category and wants to know the subcategory or product
                26) category+specs to product - Intent if the user knows the category and specifications and wants to identify the product
                27) question (generic MRO question) - Intent if the user asks a general MRO industry question
                28) chit-chat - Intent if someone engages in casual conversation or greeting
                29) unhandled services - Intent if someone asks about services not handled by the bot (e.g., post quotation, product warranty)
             '''),
        Text(id="mpn", description="Model part number of the product in the query, used to uniquely identify the product."),
        Text(id="attribute_names", description="Attribute names and details, describing the different properties that a product has (e.g., color, size)."),
        Text(id="attribute_details", description="The details attached with the attributes, including the property values (e.g., color: black)."),
        Text(id="category", description="The category of the product, representing a family of products (e.g., screw, bolt)."),
        Text(id="brand", description="The brand of the MRO industry product.")
    ],
    examples=[
        (
            "I want to buy f73#h 120 ampere ac voltage rating and 5mm thickness",
            [
                {
                    "intent": ["buy"], "mpn": "f73#h", "attribute_names": 
                    [
                        {
                            "ac voltage rating": {
                                "attribute_details": ["equals", "120 ampere"]},
                        }, 
                        {
                            "thickness": {
                                "attribute_details": ["equals", "5mm"]},
                        }
                    ]
                }                               
            ],
        ),
        (
            "Can I know the drum lifters which have load capacity > 500",
            [
                {
                    "intent": ["specifications request/question"], "category": "drum lifters", "attribute_names": [
                    {
                        "load capacity" : {
                            "attribute_details": ["greater than", "500"]
                        }
                    }
                ]
                }
            ],    
        ),
        (
            "get me quotes of vestil drum lifter 50 liters",
            [
                {
                    "intent": ["price request"], "category": "drum lifter", 
                    "attribute_names": [
                        "50 liters"
                    ],
                    "brand": "vestil"
                }
            ]
        ),
        (
            "What is the lead time for ABZE and 2UWEN?",
            [
                {"intent": ["lead time request"], "mpn": "ABZE"},
                {"intent": ["lead time request"], "mpn": "2UWEN"}
            ],
        ),
        (
            "Do you have the PD-86GAS in stock?",
            [
                {"intent": ["availability"], "mpn": "PD-86GAS"}
            ],
        ),
        (
            "Can you provide a compliance letter for the FGH-123 motor?",
            [
                {"intent": ["letter request"], "mpn": "FGH-123", "category": "motor"}
            ],
        ),
        (
            "What certifications does the ABC-321 gear motor have?",
            [
                {"intent": ["certifications / standards"], "mpn": "ABC-321", "category": "gear motor"}
            ],
        ),
        (
            "Are there any alternatives for the XYZ-987 valve?",
            [
                {"intent": ["alternate product/s request"], "mpn": "XYZ-987", "category": "valve"}
            ],
        ),
        (
            "Are there any cheaper alternatives to the XZT-123 valve?",
            [
                {"intent": ["cheaper alternative request"], "mpn": "XZT-123", "category": "valve"}
            ],
        ),
        (
            "Can you suggest a better lead time for ABC-321 gear motor?",
            [
                {"intent": ["better lead time request"], "mpn": "ABC-321", "category": "gear motor"}
            ],
        ),
        (
            "Do you have any brand alternatives for the DEF-789 hydraulic hose?",
            [
                {"intent": ["brand alternate request"], "mpn": "DEF-789", "category": "hydraulic hose"}
            ],
        ),
        (
            "I need spare parts for the LMN-456 compressor.",
            [
                {"intent": ["spare request"], "mpn": "LMN-456", "category": "compressor"}
            ],
        ),
        (
            "Can you provide a kit for the JKL-890 bearing?",
            [
                {"intent": ["kit request"], "mpn": "JKL-890", "category": "bearing"}
            ],
        ),
        (
            "Do you have any accessories for the UVW-345 filter?",
            [
                {"intent": ["accessories request"], "mpn": "UVW-345", "category": "filter"}
            ],
        ),
        (
            "What are the uses of the QRS-678 sensor?",
            [
                {"intent": ["use"], "mpn": "QRS-678", "category": "sensor"}
            ],
        ),
        (
            "Can you provide installation instructions for the NOP-234 pump?",
            [
                {"intent": ["install"], "mpn": "NOP-234", "category": "pump"}
            ],
        ),
        (
            "What is the repair procedure for the QWE-456 pump?",
            [
                {"intent": ["repair"], "mpn": "QWE-456", "category": "pump"}
            ],
        ),
        (
            "What are the uses of hydraulic hoses?",
            [
                {"intent": ["use (category)"], "category": "hydraulic hoses"}
            ],
        ),
        (
            "How do I install ball bearings?",
            [
                {"intent": ["install (category)"], "category": "ball bearings"}
            ],
        ),
        (
            "What is the repair process for pneumatic valves?",
            [
                {"intent": ["repair (category)"], "category": "pneumatic valves"}
            ],
        ),
        (
            "How does a centrifugal pump with a 10HP motor work?",
            [
                {"intent": ["use (category+specs)"], "category": "centrifugal pump", "attribute_names": [
                    {
                        "motor power": {
                            "attribute_details": ["equals", "10HP"]
                        }
                    }
                ]}
            ],
        ),
        (
            "What is the installation process for a 5kW solar inverter?",
            [
                {"intent": ["install (category+specs)"], "category": "solar inverter", "attribute_names": [
                    {
                        "power rating": {
                            "attribute_details": ["equals", "5kW"]
                        }
                    }
                ]}
            ],
        ),
        (
            "How do I repair an air compressor with a 50-gallon tank?",
            [
                {"intent": ["repair (category+specs)"], "category": "air compressor", "attribute_names": [
                    {
                        "tank capacity": {
                            "attribute_details": ["equals", "50-gallon"]
                        }
                    }
                ]}
            ],
        ),
        (
            "I need a product to measure temperature accurately.",
            [
                {"intent": ["requirement to category"], "attribute_names": ["measure", "temperature"]}
            ],
        ),
        (
            "What subcategories are there under fasteners?",
            [
                {"intent": ["category to subcategory/product"], "category": "fasteners"}
            ],
        ),
        (
            "Which product fits the category of drill bits with a 10mm diameter?",
            [
                {"intent": ["category+specs to product"], "category": "drill bits", "attribute_names": [
                    {
                        "diameter": {
                            "attribute_details": ["equals", "10mm"]
                        }
                    }
                ]}
            ],
        ),
        (
            "What are the latest trends in the MRO industry?",
            [
                {"intent": ["question (generic MRO question)"]}
            ],
        ),
        (
            "Hi there, how's it going?",
            [
                {"intent": ["chit-chat"]}
            ],
        ),
        (
            "Can you help with the warranty claim for my product?",
            [
                {"intent": ["unhandled services"], "attribute_names": ["warranty"]}
            ],
        ),
    ],
    many=True,
)



product_schema = Object(
    id="product",
    attributes=[
        intents,
    ],
    many=True,
)
