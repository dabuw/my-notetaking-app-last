# Screenshots Directory

This directory contains screenshots for the lab2_writeup.md documentation.

## Project Features to Document

The MyNoteTaking application includes several key features that should be illustrated:
- **Core Note Management**: CRUD operations, search functionality
- **AI-Powered Generation**: Natural language to structured notes conversion
- **Tag Cloud Visualization**: Interactive tag statistics and filtering
- **Responsive Design**: Desktop and mobile adaptations
- **Cloud Deployment**: Production-ready Vercel hosting

## Required Screenshots

Please add the following screenshots to illustrate the project:

### 1. main-interface.png
- Screenshot of the main application interface
- Should show the left sidebar with notes list and right panel with editor
- Demonstrate the responsive design and glass morphism effects

### 2. ai-generation.png  
- Screenshot of the AI generation feature in action
- Show the "Generate Notes" section in the sidebar
- Include example input like "今天下午5点去野餐" and the generated result

### 3. mobile-view.png
- Screenshot of the application on a mobile device
- Demonstrate responsive design adaptation for smaller screens
- Can be taken using browser developer tools mobile simulation

### 4. tag-cloud-feature.png
- Screenshot of the Tag Cloud feature in the sidebar
- Show the visual tag cloud with different sized tags based on frequency
- Demonstrate tag filtering by clicking on a tag
- Include the tag statistics display

### 5. tag-cloud-filtering.png
- Screenshot showing the tag filtering in action
- Display the filtered notes list when a tag is selected
- Show the filter indicator with "Clear Filter" button
- Demonstrate the clean editor state during filtering

### 6. vercel-deployment.png
- Screenshot of successful Vercel deployment
- Show the deployment dashboard or successful build logs
- Include the live URL: https://3dhkilc88dkk.manus.space

## How to Add Screenshots

### Taking Screenshots
1. **Start the application**: Run `python src\main.py` in the project directory
2. **Open browser**: Navigate to `http://localhost:5001`
3. **Create sample data**: Use `python create_test_data.py` to generate demo notes with tags
4. **Take screenshots**: Capture the required screenshots with exact filenames
5. **Save to directory**: Place all images in this `screenshots/` directory

### Screenshot Guidelines
- **Resolution**: Use high-resolution images (at least 1920x1080 for desktop views)
- **Content**: Ensure screenshots show meaningful data, not empty states
- **UI Elements**: Include important interface components like buttons, forms, and navigation
- **Tag Cloud**: Make sure to show tags with different sizes and the filtering functionality

### Specific Capture Instructions

#### For Tag Cloud Screenshots:
1. **Setup**: Create 5-6 notes with various tags using the test data script
2. **tag-cloud-feature.png**: 
   - Show the sidebar with populated tag cloud
   - Ensure different tag sizes are visible
   - Include the tag statistics line at bottom
3. **tag-cloud-filtering.png**:
   - Click on a popular tag to activate filtering
   - Capture the filtered notes list with filter indicator
   - Show the clear "✕ Clear Filter" button

#### For AI Generation Screenshot:
- Input example: "明天上午10点开会讨论项目进展"
- Show the generated structured output with title, content, tags, and time

## Alternative: Update Image Paths

If you prefer different filenames or locations, update the image references in `lab2_writeup.md`:

```markdown
![Description](path/to/your/screenshot.png)
```