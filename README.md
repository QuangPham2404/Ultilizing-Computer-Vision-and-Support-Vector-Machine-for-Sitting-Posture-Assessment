# **PROJECT: UTILIZING COMPUTER VISION AND SUPPORT VECTOR MACHINE FOR SITTING POSTURE ASSESSMENT**

## **ABSTRACT**

Poor sitting posture is an urgent problem on a global scale, driven by the rising prevalence of sedentary activities such as prolonged computer use. Poor sitting posture leads to work-related musculoskeletal disorders such as carpal tunnel, back injury, and back pain; cardiovascular diseases; and even permanent health damage, resulting in expensive treatments for both employers and employees. Many posture monitoring technologies rely on pressure and inertia sensors, and while these instruments are accurate, they are intrusive, expensive, and require a specialized setup, making them unsuitable for widespread deployment. Posture monitoring using cameras offers an unintrusive, cost-effective, and convenient solution while maintaining high accuracy; however, current methods are challenged by high computational demands, sensitivity to environmental conditions, and inconvenient camera placements. This paper presents a novel camera-based approach, designed to be deployed on a laptop using the built-in camera without any additional setup. First, we synthesize previous works to develop a comprehensive classification system for “correct” and “incorrect” posture. Subsequently, four numerical ratios between distances of key joint coordinates calibrated for individual users are extracted as input data for a Support Vector Machine (SVM) model to perform posture classification. By using numerical data rather than images of depth maps as input for posture-classification models, the proposed method significantly reduces the computational requirement as well as minimizes the effect of environmental variables. This approach addresses existing challenges in camera-based posture monitoring and offers a practical, efficient solution for real-time sitting posture assessment. Furthermore, this paper also discusses utilizing the lightweight computational load of the SVM model for deployment on edge-AI modules, enabling a portable and robust sitting posture assessment system.

**Progress Report Link:** [LINK](https://docs.google.com/document/d/19jx68Y5_j-Ulr1dCGZ0WGKnvGe7lnnX2iYIdK7WnP-8/edit?tab=t.0)

## **PROJECT DETAILS**

## **I. Problem statement and Contributions**

Poor sitting posture, including slouching, hunching, sitting with head tilted heavily forward, etc, is a pressing issue among Vietnamese, especially among students. It is the main factor of scoliosis, which the Commission for Information and Education reported to affect 1.3% to 36.33% of the students in major cities in Vietnam in 2022. This is an alarming rise from 7.4% in 2019, and the number is expected to continue to increase in the future. 

Poor sitting posture is also an urgent problem on the global scale. Due to the pandemic, the time people spend in sedentary activities such as sitting and working on a computer for a long period has increased considerably. According to Vermander et al. (2024), nowadays people spend more than half of their daily hours in a seated position, reaching up to 85% of their hours in the case of people with low mobility. Nadeem M. et al. (2024) stated an average office worker in today’s world uses up to 75% of their day sitting, with over half of that time occurring during extended periods of almost complete inactivity. This will eventually lead to work-related musculoskeletal disorders (Rodrigues P. et al., 2022), cardiovascular diseases (CVDs), metabolic syndrome, diabetes, and hypertension (Estrada J. et al., 2023) if the posture is not carefully monitored. Furthermore, poor posture causes musculoskeletal disorders such as carpal tunnel, back injury, and back pain and also permanent damage to health, resulting in a great amount of expenses for treatments for both employers and employees (Ding Z. et al., 2019). Several medical studies have proven that bad posture after long periods results in major back/neck problems (Kapoor R. et al., 2022), as multiple studies showed that 17.7–63% of office workers experienced neck pain, and 23–34% suffered from back pain (Estrada J. et al., 2023). As the number of people who will sit and work in front of a computer will increase in the future, and many of them do not have the knowledge on how to maintain proper posture (Kapoor R. et al., 2022) or are occupied with work to effectively adhere to ergonomic rules, _a need for efficient and convenient sitting posture monitor systems is evident_.

Current methods that rely on sensors (e.g. pressure and inertia sensors), despite achieving high accuracy, are expensive, intrusive, and require specialized set-up, making them unsuitable for widespread use. Camera-based methods, on the other hand, offer a more cost-effective and convenient approach; however, existing approaches face difficulties due to significant computational requirements, susceptibility to environmental factors (e.g. lighting conditions), and inconvenient camera positioning.

This research addresses the gaps identified through the following contributions:
1. We developed a comprehensive system for classifying “correct” and “incorrect” sitting posture classifying system by synthesizing previous works.
2. We proposed a novel camera-based approach, which utilizes four numerical ratios of distances between key joints calibrated individually for each user, and a Support Vector Machine (SVM) model to perform cost-effective sitting posture monitoring. By using numerical data rather than images or depth maps like the previous approach, the computation weight is reduced considerably, and the effect of environmental factors is lessened. Moreover, the system is designed to be deployed on built-in cameras in laptops, offering convenience for users without needing additional hardware setup.
4. After the system is tested for effectiveness, we outlined a potential design to deploy the system on an edge AI-integrated camera PCB module, allowing for deployment in scenarios beyond computer use, such as for students working on notebooks or textbooks in classrooms. The proposed camera module can operate independently, offering robust and real-time posture assessment in diverse environments.

With these contributions, our research aims to make posture monitoring accessible and practical for a broad audience, promoting better sitting habits and reducing posture-related health issues around the world.

## **II. Codes explanation**

### 1. Libraries used

This project uses the following libraries/packages:
1. cv2 library: for obtaining real-time input video stream from webcam and processing each frame in the video stream
2. mediapipe library: uses Pose Landmarker Model to detect key joints coordinates to calculate feature data for SVM model
3. win10toast library: for notifying the user when incorrect posture is detected
4. joblib library: for saving and loading the trained SVM model as a .pkl file
5. numpy library: for handling SVM input vectors
6. os library: for navigating and making changes in directory (combine files, etc)

### 2. Programs details

There are 3 main programs used for training and deploying the Support Vector Machine (SVM) for real-time sitting posture classification.

1. ***a_get_training_data.py***: This program is for collecting and preparing training and testing data for the Support Vector Machine (SVM) model used in sitting posture classification. When run for each subject participating in the study, the script extracts feature values and saves them in a .txt file named _[Subject_name]_data.tx_t. Simultaneously, it generates a corresponding .txt file containing the labels (0s for correct posture, 1s for incorrect posture), named _[Subject_name]_tag.txt_. For example, the files _Quang_data.txt_ and _Quang_tag.txt_ represent the feature data and labels for a subject named Quang. After processing individual subjects, the program automatically consolidates all the data files and tag files into two comprehensive .txt files: _combined_data.txt_ and _combined_tag.txt_. These combined files serve as the complete dataset for training and testing the SVM model, ensuring an efficient and organized workflow for data
2. ***b_get_SVM.py***: This program is for training the SVM model and saving it as a .pkl file for further usage. After completing the training data files with _a_get_training_data.py_, run this program to train the SVM.
3. ***c_classify_posture.py***: This program is for deploying the SVM on the laptop's webcam to classify sitting posture as "correct" or "incorrect" in real-time. If "incorrect" posture is detected for 10s straight, a Window pop-up warning message will be created. If the user does not fix their posture for the next 5s, another pop-up warning message will be created until they fix their sitting posture to "correct."

The remaning files are for experimenting when developing the approach:
1. ***pose_detection_practice.py***: This program is for experimenting with MediaPipe Pose Landmarker Model and different feature data values for sitting posture classification.
2. ***data_visualization.py***: This program is for experimenting with different feature data values by exmaining their characteristics corresponding to the change in sitting posture.

## III. Progress Update

The project is still in development. Currently we are expanding the training dataset to train the SVM model. For the detailed timeline for future plans please refer to the [Progress Report](https://docs.google.com/document/d/19jx68Y5_j-Ulr1dCGZ0WGKnvGe7lnnX2iYIdK7WnP-8/edit?tab=t.0).













 


