resource "google_bigquery_table" "query_table" {
  dataset_id = "usecase_dataset"
  table_id   = "usecase_table"
  project=var.project_id
  deletion_protection=false
  clustering=["Category","Sub_Category"]
  depends_on = [
    google_bigquery_dataset.aaron_dataset
  ]

  schema = <<EOF
  [
  {
    "name": "Contributor",
    "type": "STRING",
    "mode": "NULLABLE"
    
  },
  {
    "name": "Sub_Category",
    "type": "STRING",
    "mode": "REQUIRED"
    
  },
  {
    "name": "Category",
    "type": "STRING",
    "mode": "REQUIRED"
        
  },
  {
    "name": "Multiplying_Factor",
    "type": "INTEGER",
    "mode": "NULLABLE"
    
  },
   {
    "name": "Area_code",
    "type": "STRING",
    "mode": "NULLABLE"
   
  },
  {
    "name": "Feature_Factors",
    "type": "RECORD",
    "mode": "NULLABLE",
    "fields": [
            {
                "name": "Feature_1",
                "type": "FLOAT",
                "mode": "NULLABLE"
            },
            {
                "name": "Feature_2",
                "type": "FLOAT",
                "mode": "NULLABLE"
            },
            {
                "name": "Feature_3",
                "type": "INTEGER",
                "mode": "REPEATED"
            }
        ]
  }
  
]
EOF

}

resource "google_bigquery_dataset" "aaron_dataset" {
  dataset_id                  = "sustain_it_dataset"
  friendly_name               = "test"
  description                 = "use-case dataset"
  location                    = var.region
  project                     = var.project_id
  provider                    = google
  

  labels = {
    env = "default"
  }
  access {
    role          = "OWNER"
    user_by_email = "aaron.john@sada.com"
  } 
}
  