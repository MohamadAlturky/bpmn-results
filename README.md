# bpmn-results

> the files contains the samples that we will evaluate the model on.


## src
>process_files.py contains the code for convert the PET json objects to more understandable objects

## each folder with number {num} contains four files
- row_{num}.json: is the record from PET dataset
- row_{num}.txt: contains the process description
- reult_row_{num}.json: contains converted json from PET to more understandable object
- generated_row_{num}.json: contains the generated diagram by our model

# Notes
## we put ✅ in the result_row_{num}.json file if the bpmn component found
