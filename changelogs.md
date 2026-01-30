# Change Logs

- [Change Logs](#change-logs)
  - [Updates (DD/MM/YY)](#updates-ddmmyy)
    - [Update Date : 31/01/2026](#update-date--31012026)
    - [Update Date : 03/08/2023](#update-date--03082023)
    - [Update Date : 24/05/2023](#update-date--24052023)
    - [Update Date : 27/04/2023](#update-date--27042023)


## Updates (DD/MM/YY)

### Update Date : 31/01/2026

- VenvManager is refactored.
- Multi-architecture model loading is added with
  [spandrel](https://github.com/chaiNNer-org/spandrel) package.
- Some PyTorch optimizations are added like `torch.compile`.
- Tiling upscaling support is added.
- The scale variable is default to model's supported scale.
- Recursion image file location functionality is added.
- New models and architectures are added.
- Model download automation is added.
- Torch data type selection is added.

### Update Date : 03/08/2023

- VenvManager is added. Don't have to press **Startup** button after starting.
  It is handled by VenvManager.
- Logging system is updated.
- Tiling is done by default.

### Update Date : 24/05/2023

- Not using GPU bug is fixed. Delete Real-ESRGAN folder and click **Startup**
  button.
- As a note, if you have encountered with black output, select FP32 option.

### Update Date : 27/04/2023

- Modern GUI style is added with customtkinter
- Virtual environment automation is added. No need to configure manually. Just
  run `python start.py` command.
- **Startup** and **Initialize** functions are done in threads so no more
  freezing.
- Selection for FP32 feature is added.
- [x] I did not hide the command outputs because some processes take minutes and
      it makes it difficult to understand what is going on. If there are no
      errors and application is not terminated, it is fine.

<p align="center">
  <img src=https://user-images.githubusercontent.com/76731692/234876288-9a368045-10a5-4455-997c-c0f8553ab9a4.gif alt="animated" />
</p>
