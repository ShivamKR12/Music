# KivyMD API Reference

> Automatically generated from the KivyMD documentation.
> Source: https://kivymd.readthedocs.io/en/latest/

---

## API - [`kivymd`](https://kivymd.readthedocs.io/en/latest/api/kivymd/)

**kivymd.path**

Path to KivyMD package directory.

**kivymd.fonts_path**

Path to fonts directory.

**kivymd.images_path**

Path to images directory.

**kivymd.uix_path**

Path to uix directory.

**kivymd.glsl_path**

Path to glsl directory.

---

## API - [`kivymd.animation`](https://kivymd.readthedocs.io/en/latest/components/animation/)

**kivymd.animation.MDAnimationTransition**

KivyMD’s equivalent of kivy’s AnimationTransition.

**kivymd.animation.MDAnimationTransition.easing_standard**

Material Design standard easing transition.
[`easing_standard`](https://kivymd.readthedocs.io/en/latest/#kivymd.animation.MDAnimationTransition.easing_standard) is a `Callable` and defaults to
`CubicBezier(0.4, 0.0, 0.2, 1.0).t`.

**kivymd.animation.MDAnimationTransition.easing_decelerated**

Material Design standard easing transition.
[`easing_decelerated`](https://kivymd.readthedocs.io/en/latest/#kivymd.animation.MDAnimationTransition.easing_decelerated) is a `Callable` and defaults to
`CubicBezier(0.0, 0.0, 0.2, 1.0).t`.

**kivymd.animation.MDAnimationTransition.easing_accelerated**

Material Design standard easing transition.
[`easing_accelerated`](https://kivymd.readthedocs.io/en/latest/#kivymd.animation.MDAnimationTransition.easing_accelerated) is a `Callable` and defaults to
`CubicBezier(0.4, 0.0, 1.0, 1.0).t`.

**kivymd.animation.MDAnimationTransition.easing_linear**

Material Design standard easing transition.
[`easing_linear`](https://kivymd.readthedocs.io/en/latest/#kivymd.animation.MDAnimationTransition.easing_linear) is a `Callable` and defaults to
`CubicBezier(0.0, 0.0, 1.0, 1.0).t`.

**kivymd.animation.MDAnimationTransition.easing_emphasized**

Material Design emphasized easing transition.

---

## API - [`kivymd.dynamic_color`](https://kivymd.readthedocs.io/en/latest/components/dynamic-color/)

**kivymd.dynamic_color.DynamicColor**

Dynamic color class.
Added in version 2.0.0.

**kivymd.dynamic_color.DynamicColor.current_schemes_color_data**

**kivymd.dynamic_color.DynamicColor.primaryColor**

Primary color.
[`primaryColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.primaryColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.primaryDimColor**

Primary dim color.
[`primaryDimColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.primaryDimColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.primaryContainerColor**

Primary container color.
[`primaryContainerColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.primaryContainerColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onPrimaryColor**

On primary color.
[`onPrimaryColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onPrimaryColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onPrimaryContainerColor**

On primary container color.
[`onPrimaryContainerColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onPrimaryContainerColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.primaryFixedColor**

Primary fixed color.
[`primaryFixedColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.primaryFixedColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.primaryFixedDimColor**

Primary fixed dim color.
[`primaryFixedDimColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.primaryFixedDimColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onPrimaryFixedColor**

On primary fixed color.
[`onPrimaryFixedColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onPrimaryFixedColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onPrimaryFixedVariantColor**

On primary fixed variant color.
[`onPrimaryFixedVariantColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onPrimaryFixedVariantColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.secondaryColor**

Secondary color.
[`secondaryColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.secondaryColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.secondaryDimColor**

Secondary dim color.
[`secondaryDimColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.secondaryDimColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.secondaryContainerColor**

Secondary container color.
[`secondaryContainerColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.secondaryContainerColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onSecondaryColor**

On secondary color.
[`onSecondaryColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onSecondaryColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onSecondaryContainerColor**

On secondary container color.
[`onSecondaryContainerColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onSecondaryContainerColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.secondaryFixedColor**

Secondary fixed color.
[`secondaryFixedColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.secondaryFixedColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.secondaryFixedDimColor**

Secondary fixed dim color.
[`secondaryFixedDimColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.secondaryFixedDimColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onSecondaryFixedColor**

On secondary fixed color.
[`onSecondaryFixedColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onSecondaryFixedColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onSecondaryFixedVariantColor**

On secondary fixed variant color.
[`onSecondaryFixedVariantColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onSecondaryFixedVariantColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.tertiaryColor**

Tertiary color.
[`tertiaryColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.tertiaryColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.tertiaryDimColor**

Tertiary dim color.
[`tertiaryDimColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.tertiaryDimColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.tertiaryContainerColor**

Tertiary container color.
[`tertiaryContainerColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.tertiaryContainerColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onTertiaryColor**

On tertiary color.
[`onTertiaryColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onTertiaryColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onTertiaryContainerColor**

On tertiary container color.
[`onTertiaryContainerColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onTertiaryContainerColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.tertiaryFixedColor**

Tertiary fixed color.
[`tertiaryFixedColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.tertiaryFixedColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.tertiaryFixedDimColor**

Tertiary fixed dim color.
[`tertiaryFixedDimColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.tertiaryFixedDimColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onTertiaryFixedColor**

On tertiary fixed color.
[`onTertiaryFixedColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onTertiaryFixedColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onTertiaryFixedVariantColor**

On tertiary fixed variant color.
[`onTertiaryFixedVariantColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onTertiaryFixedVariantColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.surfaceColor**

Surface color.
[`surfaceColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.surfaceColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.surfaceDimColor**

Surface dim color.
[`surfaceDimColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.surfaceDimColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.surfaceBrightColor**

Surface bright color.
[`surfaceBrightColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.surfaceBrightColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.surfaceContainerLowestColor**

Surface container lowest color.
[`surfaceContainerLowestColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.surfaceContainerLowestColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.surfaceContainerLowColor**

Surface container low color.
[`surfaceContainerLowColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.surfaceContainerLowColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.surfaceContainerColor**

Surface container color.
[`surfaceContainerColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.surfaceContainerColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.surfaceContainerHighColor**

Surface container high color.
[`surfaceContainerHighColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.surfaceContainerHighColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.surfaceContainerHighestColor**

Surface container highest color.
[`surfaceContainerHighestColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.surfaceContainerHighestColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.surfaceVariantColor**

Surface variant color.
[`surfaceVariantColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.surfaceVariantColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.surfaceTintColor**

Surface tint color.
[`surfaceTintColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.surfaceTintColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onSurfaceColor**

On surface color.
[`onSurfaceColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onSurfaceColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onSurfaceLightColor**

On surface light color.
[`onSurfaceLightColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onSurfaceLightColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onSurfaceVariantColor**

On surface variant color.
[`onSurfaceVariantColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onSurfaceVariantColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.inverseSurfaceColor**

Inverse surface color.
[`inverseSurfaceColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.inverseSurfaceColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.inverseOnSurfaceColor**

Inverse on surface color.
[`inverseOnSurfaceColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.inverseOnSurfaceColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.inversePrimaryColor**

Inverse primary color.
[`inversePrimaryColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.inversePrimaryColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.backgroundColor**

Background color.
[`backgroundColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.backgroundColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onBackgroundColor**

On background color.
[`onBackgroundColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onBackgroundColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.errorColor**

Error color.
[`errorColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.errorColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.errorDimColor**

Error dim color.
[`errorDimColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.errorDimColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.errorContainerColor**

Error container color.
[`errorContainerColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.errorContainerColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onErrorColor**

On error color.
[`onErrorColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onErrorColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.onErrorContainerColor**

On error container color.
[`onErrorContainerColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.onErrorContainerColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.outlineColor**

Outline color.
[`outlineColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.outlineColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.outlineVariantColor**

Outline variant color.
[`outlineVariantColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.outlineVariantColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.shadowColor**

Shadow color.
[`shadowColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.shadowColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.scrimColor**

Scrim color.
[`scrimColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.scrimColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.primaryPaletteKeyColorColor**

Primary palette key color.
[`primaryPaletteKeyColorColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.primaryPaletteKeyColorColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.secondaryPaletteKeyColorColor**

Secondary palette key color.
[`secondaryPaletteKeyColorColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.secondaryPaletteKeyColorColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.tertiaryPaletteKeyColorColor**

Tertiary palette key color.
[`tertiaryPaletteKeyColorColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.tertiaryPaletteKeyColorColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.neutralPaletteKeyColorColor**

Neutral palette key color.
[`neutralPaletteKeyColorColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.neutralPaletteKeyColorColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.neutralVariantPaletteKeyColorColor**

Neutral variant palette key color.
[`neutralVariantPaletteKeyColorColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.neutralVariantPaletteKeyColorColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.errorPaletteKeyColorColor**

Error palette key color.
[`errorPaletteKeyColorColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.errorPaletteKeyColorColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.disabledTextColor**

Disabled text color.
[`disabledTextColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.disabledTextColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.dynamic_color.DynamicColor.transparentColor**

Transparent color.
[`transparentColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.transparentColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to [0, 0, 0, 0].

**kivymd.dynamic_color.DynamicColor.rippleColor**

Ripple color.
[`rippleColor`](https://kivymd.readthedocs.io/en/latest/#kivymd.dynamic_color.DynamicColor.rippleColor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to ‘#BDBDBD’.

---

## API - [`kivymd.factory_registers`](https://kivymd.readthedocs.io/en/latest/api/kivymd/factory_registers/)

**kivymd.factory_registers.register**

---

## API - [`kivymd.material_resources`](https://kivymd.readthedocs.io/en/latest/api/kivymd/material_resources/)

**kivymd.material_resources.dp**

**kivymd.material_resources.DEVICE_IOS**

**kivymd.material_resources.DEVICE_TYPE**

---

## API - [`kivymd.toast.androidtoast`](https://kivymd.readthedocs.io/en/latest/api/kivymd/toast/androidtoast/)

**kivymd.toast.androidtoast.toast**

Displays a toast.

Important: if only the text value is specified and the value of
the gravity, y, x parameters is not specified, their values will
be 0 which means that the toast will be shown in the center.

---

## API - [`kivymd.tools.argument_parser`](https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/argument_parser/)

**kivymd.tools.argument_parser.ArgumentParserWithHelp**

Object for parsing command line strings into Python objects.

**kivymd.tools.argument_parser.ArgumentParserWithHelp.parse_args**

**kivymd.tools.argument_parser.ArgumentParserWithHelp.error**

error(message: string)
Prints a usage message incorporating the message to stderr and
exits.
If you override this in a subclass, it should not return – it
should either exit or raise an exception.

**kivymd.tools.argument_parser.ArgumentParserWithHelp.format_help**

---

## API - [`kivymd.tools.hotreload.app`](https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/hotreload/app/)

**kivymd.tools.hotreload.app.original_argv**

**kivymd.tools.hotreload.app.monotonic**

**kivymd.tools.hotreload.app.PY3**

**kivymd.tools.hotreload.app.ExceptionClass**

Base handler that catches exceptions in `runTouchApp()`.
You can subclass and extend it as follows:

Then, all exceptions will be set to PASS, and logged to the console!

**kivymd.tools.hotreload.app.ExceptionClass.handle_exception**

Called by `ExceptionManagerBase` to handle a exception.
Defaults to returning `ExceptionManager.RAISE` that re-raises the
exception. Return `ExceptionManager.PASS` to indicate that the
exception was handled and should be ignored.
This may be called multiple times with the same exception, if
`ExceptionManager.RAISE` is returned as the exception bubbles
through multiple kivy exception handling levels.

**kivymd.tools.hotreload.app.MDApp**

HotReload Application class.

**kivymd.tools.hotreload.app.MDApp.appname**

Return the name of the application class.

**kivymd.tools.hotreload.app.MDApp.DEBUG**

Control either we activate debugging in the app or not.
Defaults depend if ‘DEBUG’ exists in os.environ.
[`DEBUG`](https://kivymd.readthedocs.io/en/latest/#kivymd.tools.hotreload.app.MDApp.DEBUG) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty).

**kivymd.tools.hotreload.app.MDApp.FOREGROUND_LOCK**

If True it will require the foreground lock on windows.
[`FOREGROUND_LOCK`](https://kivymd.readthedocs.io/en/latest/#kivymd.tools.hotreload.app.MDApp.FOREGROUND_LOCK) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.tools.hotreload.app.MDApp.KV_FILES**

List of KV files under management for auto reloader.
[`KV_FILES`](https://kivymd.readthedocs.io/en/latest/#kivymd.tools.hotreload.app.MDApp.KV_FILES) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [].

**kivymd.tools.hotreload.app.MDApp.KV_DIRS**

List of managed KV directories for autoloader.
[`KV_DIRS`](https://kivymd.readthedocs.io/en/latest/#kivymd.tools.hotreload.app.MDApp.KV_DIRS) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [].

**kivymd.tools.hotreload.app.MDApp.AUTORELOADER_PATHS**

List of path to watch for auto reloading.
[`AUTORELOADER_PATHS`](https://kivymd.readthedocs.io/en/latest/#kivymd.tools.hotreload.app.MDApp.AUTORELOADER_PATHS) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to ([(“.”, {“recursive”: True})].

**kivymd.tools.hotreload.app.MDApp.AUTORELOADER_IGNORE_PATTERNS**

List of extensions to ignore.
[`AUTORELOADER_IGNORE_PATTERNS`](https://kivymd.readthedocs.io/en/latest/#kivymd.tools.hotreload.app.MDApp.AUTORELOADER_IGNORE_PATTERNS) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [‘*.pyc’, ‘*__pycache__*’].

**kivymd.tools.hotreload.app.MDApp.CLASSES**

Factory classes managed by hotreload.
[`CLASSES`](https://kivymd.readthedocs.io/en/latest/#kivymd.tools.hotreload.app.MDApp.CLASSES) is a [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty)
and defaults to {}.

**kivymd.tools.hotreload.app.MDApp.IDLE_DETECTION**

Idle detection (if True, event on_idle/on_wakeup will be fired).
Rearming idle can also be done with rearm_idle().
[`IDLE_DETECTION`](https://kivymd.readthedocs.io/en/latest/#kivymd.tools.hotreload.app.MDApp.IDLE_DETECTION) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.tools.hotreload.app.MDApp.IDLE_TIMEOUT**

Default idle timeout.
[`IDLE_TIMEOUT`](https://kivymd.readthedocs.io/en/latest/#kivymd.tools.hotreload.app.MDApp.IDLE_TIMEOUT) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 60.

**kivymd.tools.hotreload.app.MDApp.RAISE_ERROR**

Raise error.
When the DEBUG is activated, it will raise any error instead
of showing it on the screen. If you still want to show the error
when not in DEBUG, put this to False.
[`RAISE_ERROR`](https://kivymd.readthedocs.io/en/latest/#kivymd.tools.hotreload.app.MDApp.RAISE_ERROR) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivymd.tools.hotreload.app.MDApp.build**

Initializes the application; it will be called only once.
If this method returns a widget (tree), it will be used as the root
widget and added to the window.

**kivymd.tools.hotreload.app.MDApp.get_root**

Return a root widget, that will contains your application.
It should not be your application widget itself, as it may
be destroyed and recreated from scratch when reloading.
By default, it returns a RelativeLayout, but it could be
a Viewport.

**kivymd.tools.hotreload.app.MDApp.get_root_path**

Return the root file path.

**kivymd.tools.hotreload.app.MDApp.build_app**

Must return your application widget.
If first is set, it means that will be your first time ever
that the application is built. Act according to it.

**kivymd.tools.hotreload.app.MDApp.unload_app_dependencies**

Called when all the application dependencies must be unloaded.
Usually happen before a reload

**kivymd.tools.hotreload.app.MDApp.load_app_dependencies**

Load all the application dependencies.
This is called before rebuild.

**kivymd.tools.hotreload.app.MDApp.rebuild**

**kivymd.tools.hotreload.app.MDApp.set_error**

**kivymd.tools.hotreload.app.MDApp.bind_key**

Bind a key (keycode) to a callback (cannot be unbind).

**kivymd.tools.hotreload.app.MDApp.enable_autoreload**

Enable autoreload manually. It is activated automatically
if “DEBUG” exists in environ. It requires the watchdog module.

**kivymd.tools.hotreload.app.MDApp.prepare_foreground_lock**

Try forcing app to front permanently to avoid windows
pop ups and notifications etc.app.
Requires fake full screen and borderless.

**kivymd.tools.hotreload.app.MDApp.set_widget**

Clear the root container, and set the new approot widget to wid.

**kivymd.tools.hotreload.app.MDApp.apply_state**

Whatever the current state is, reapply the current state.

**kivymd.tools.hotreload.app.MDApp.install_idle**

Install the idle detector. Default timeout is 60s.
Once installed, it will check every second if the idle timer
expired. The timer can be rearm using [`rearm_idle()`](https://kivymd.readthedocs.io/en/latest/#kivymd.tools.hotreload.app.MDApp.rearm_idle).

**kivymd.tools.hotreload.app.MDApp.rearm_idle**

Rearm the idle timer.

**kivymd.tools.hotreload.app.MDApp.patch_builder**

**kivymd.tools.hotreload.app.MDApp.on_idle**

Event fired when the application enter the idle mode.

**kivymd.tools.hotreload.app.MDApp.on_wakeup**

Event fired when the application leaves idle mode.

---

## API - [`kivymd.tools.packaging.pyinstaller`](https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/packaging/pyinstaller/)

**kivymd.tools.packaging.pyinstaller.hooks_path**

Path to hook directory to use with PyInstaller.
See [`kivymd.tools.packaging.pyinstaller`](https://kivymd.readthedocs.io/en/latest/#module-kivymd.tools.packaging.pyinstaller) for more information.

**kivymd.tools.packaging.pyinstaller.get_hook_dirs**

**kivymd.tools.packaging.pyinstaller.get_pyinstaller_tests**

---

## API - [`kivymd.tools.packaging.pyinstaller.hook-kivymd`](https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/packaging/pyinstaller/hook-kivymd/)

**kivymd.tools.packaging.pyinstaller.hook-kivymd.datas**

---

## API - [`kivymd.tools.patterns.add_view`](https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/patterns/add_view/)

**kivymd.tools.patterns.add_view.main**

The function of adding a new view to the project.

---

## API - [`kivymd.tools.patterns.create_project`](https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/patterns/create_project/)

**kivymd.tools.patterns.create_project.main**

Project creation function.

---

## API - [`kivymd.tools.patterns.MVC.libs.translation`](https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/patterns/MVC/libs/translation/)

**kivymd.tools.patterns.MVC.libs.translation.Translation**

Original source - [tito/kivy-gettext-example](https://github.com/tito/kivy-gettext-example).

**kivymd.tools.patterns.MVC.libs.translation.Translation.observers**

**kivymd.tools.patterns.MVC.libs.translation.Translation.fbind**

**kivymd.tools.patterns.MVC.libs.translation.Translation.funbind**

**kivymd.tools.patterns.MVC.libs.translation.Translation.switch_lang**

---

## API - [`kivymd.tools.patterns.MVC.Model.database_firebase`](https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/patterns/MVC/Model/database_firebase/)

**kivymd.tools.patterns.MVC.Model.database_firebase.get_connect**

Checks for an active Internet connection.

**kivymd.tools.patterns.MVC.Model.database_firebase.DataBase**

Your methods for working with the database should be implemented in this
class.

**kivymd.tools.patterns.MVC.Model.database_firebase.DataBase.name**

**kivymd.tools.patterns.MVC.Model.database_firebase.DataBase.get_data_from_collection**

Returns data of the selected collection from the database.

---

## API - [`kivymd.tools.patterns.MVC.Model.database_restdb`](https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/patterns/MVC/Model/database_restdb/)

**kivymd.tools.patterns.MVC.Model.database_restdb.get_connect**

Checks for an active Internet connection.

**kivymd.tools.patterns.MVC.Model.database_restdb.DataBase**

**kivymd.tools.patterns.MVC.Model.database_restdb.DataBase.name**

**kivymd.tools.patterns.MVC.Model.database_restdb.DataBase.upload_file**

Uploads a file to the database.
You can upload a file to the database only from a paid account.

**kivymd.tools.patterns.MVC.Model.database_restdb.DataBase.get_data_from_collection**

Returns data of the selected collection from the database.

**kivymd.tools.patterns.MVC.Model.database_restdb.DataBase.delete_doc_from_collection**

Delete data of the selected collection from the database.

**kivymd.tools.patterns.MVC.Model.database_restdb.DataBase.add_doc_to_collection**

Add collection to the database.

**kivymd.tools.patterns.MVC.Model.database_restdb.DataBase.edit_data**

Modifies data in a collection of data in a database.

---

## API - [`kivymd.tools.release.git_commands`](https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/release/git_commands/)

**kivymd.tools.release.git_commands.command**

Run system command.

**kivymd.tools.release.git_commands.get_previous_version**

Returns latest tag in git.

**kivymd.tools.release.git_commands.git_clean**

Clean git repository from untracked and changed files.

**kivymd.tools.release.git_commands.git_commit**

Make commit.

**kivymd.tools.release.git_commands.git_tag**

Create tag.

**kivymd.tools.release.git_commands.git_push**

Push all changes.

---

## API - [`kivymd.tools.release.make_release`](https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/release/make_release/)

**kivymd.tools.release.make_release.run_pre_commit**

Run pre-commit.

**kivymd.tools.release.make_release.replace_in_file**

Replace one pattern match to repl in file file.

**kivymd.tools.release.make_release.update_version_py**

Change version in kivymd/_version.py.

**kivymd.tools.release.make_release.update_readme**

Change version in README.md.

**kivymd.tools.release.make_release.move_changelog**

Edit unreleased.rst and rename to <version>.rst.

**kivymd.tools.release.make_release.create_unreleased_changelog**

Create unreleased.rst by template.

**kivymd.tools.release.make_release.main**

**kivymd.tools.release.make_release.create_argument_parser**

---

## API - [`kivymd.tools.release.update_icons`](https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/release/update_icons/)

**kivymd.tools.release.update_icons.kivymd_path**

**kivymd.tools.release.update_icons.font_path**

**kivymd.tools.release.update_icons.icon_definitions_path**

**kivymd.tools.release.update_icons.font_version**

**kivymd.tools.release.update_icons.url**

**kivymd.tools.release.update_icons.temp_path**

**kivymd.tools.release.update_icons.temp_repo_path**

**kivymd.tools.release.update_icons.temp_font_path**

**kivymd.tools.release.update_icons.temp_preview_path**

**kivymd.tools.release.update_icons.re_icons_json**

**kivymd.tools.release.update_icons.re_additional_icons**

**kivymd.tools.release.update_icons.re_version**

**kivymd.tools.release.update_icons.re_quote_keys**

**kivymd.tools.release.update_icons.re_icon_definitions**

**kivymd.tools.release.update_icons.re_version_in_file**

**kivymd.tools.release.update_icons.download_file**

**kivymd.tools.release.update_icons.unzip_archive**

**kivymd.tools.release.update_icons.get_icons_list**

**kivymd.tools.release.update_icons.make_icon_definitions**

**kivymd.tools.release.update_icons.export_icon_definitions**

**kivymd.tools.release.update_icons.update_icons**

**kivymd.tools.release.update_icons.main**

---

## API - [`kivymd.uix`](https://kivymd.readthedocs.io/en/latest/api/kivymd/uix/)

**kivymd.uix.MDAdaptiveWidget**

**kivymd.uix.MDAdaptiveWidget.adaptive_height**

If True, the following properties will be applied to the widget:

[`adaptive_height`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.MDAdaptiveWidget.adaptive_height) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.MDAdaptiveWidget.adaptive_width**

If True, the following properties will be applied to the widget:

[`adaptive_width`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.MDAdaptiveWidget.adaptive_width) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.MDAdaptiveWidget.adaptive_size**

If True, the following properties will be applied to the widget:

[`adaptive_size`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.MDAdaptiveWidget.adaptive_size) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.MDAdaptiveWidget.on_adaptive_height**

**kivymd.uix.MDAdaptiveWidget.on_adaptive_width**

**kivymd.uix.MDAdaptiveWidget.on_adaptive_size**

---

## API - [`kivymd.uix.anchorlayout`](https://kivymd.readthedocs.io/en/latest/components/anchorlayout/)

**kivymd.uix.anchorlayout.MDAnchorLayout**

Anchor layout class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`AnchorLayout`](https://kivy.org/doc/stable/api-kivy.uix.anchorlayout.html#kivy.uix.anchorlayout.AnchorLayout) and
[`MDAdaptiveWidget`](https://kivymd.readthedocs.io/api/kivymd/uix/#kivymd.uix.MDAdaptiveWidget)
classes documentation.

---

## API - [`kivymd.uix.appbar.appbar`](https://kivymd.readthedocs.io/en/latest/components/appbar/)

**kivymd.uix.appbar.appbar.MDFabBottomAppBarButton**

Implements a floating action button (FAB) for a bar with type ‘bottom’.
For more information, see in the
[`MDFabButton`](https://kivymd.readthedocs.io/en/button/#kivymd.uix.button.button.MDFabButton) and
[`RotateBehavior`](https://kivymd.readthedocs.io/behaviors/rotate/#kivymd.uix.behaviors.rotate_behavior.RotateBehavior) and
[`ScaleBehavior`](https://kivymd.readthedocs.io/behaviors/scale/#kivymd.uix.behaviors.scale_behavior.ScaleBehavior) and
classes documentation.

**kivymd.uix.appbar.appbar.MDActionTopAppBarButton**

Implements action buttons on the bar.
For more information, see in the
[`MDIconButton`](https://kivymd.readthedocs.io/en/button/#kivymd.uix.button.button.MDIconButton) class documentation.

**kivymd.uix.appbar.appbar.MDActionTopAppBarButton.md_bg_color_disabled**

The background color in (r, g, b, a) or string format of the button when
the button is disabled.
[`md_bg_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDActionTopAppBarButton.md_bg_color_disabled) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.appbar.appbar.MDActionBottomAppBarButton**

Implements action buttons for a
:class:’~kivymd.uix.appbar.appbar.MDBottomAppBar’ class.
Added in version 1.2.0.
For more information, see in the
[`MDActionTopAppBarButton`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDActionTopAppBarButton)
class documentation.

**kivymd.uix.appbar.appbar.MDTopAppBarTitle**

Implements the panel title.
Added in version 2.0.0.
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) class documentation.

**kivymd.uix.appbar.appbar.MDTopAppBarLeadingButtonContainer**

Implements a container for the leading action buttons.
Added in version 2.0.0.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
classes documentation.

**kivymd.uix.appbar.appbar.MDTopAppBarTrailingButtonContainer**

Implements a container for the trailing action buttons.
Added in version 2.0.0.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
classes documentation.

**kivymd.uix.appbar.appbar.MDTopAppBar**

Top app bar class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`CommonElevationBehavior`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout) and
[`WindowController`](https://kivymd.readthedocs.io/controllers/windowcontroller/#kivymd.uix.controllers.windowcontroller.WindowController)
classes documentation.

**kivymd.uix.appbar.appbar.MDTopAppBar.set_bars_color**

If True the background color of the bar status will be set automatically
according to the current color of the bar.
Added in version 1.0.0.
See [set_bars_colors](https://kivymd.readthedocs.io/en/latest/api/kivymd/utils/set_bars_colors/)
for more information.
[`set_bars_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDTopAppBar.set_bars_color) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.appbar.appbar.MDTopAppBar.type**

Bar height type.
Added in version 1.0.0.
Available options are: ‘medium’, ‘large’, ‘small’.
`type_height` is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘small’.

**kivymd.uix.appbar.appbar.MDTopAppBar.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.appbar.appbar.MDBottomAppBar**

Bottom app bar class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`CommonElevationBehavior`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior) and
[`FloatLayout`](https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html#kivy.uix.floatlayout.FloatLayout)
classes documentation.

**kivymd.uix.appbar.appbar.MDBottomAppBar.action_items**

The icons on the left bar.
Added in version 1.2.0.
[`action_items`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar.action_items) is an [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [].

**kivymd.uix.appbar.appbar.MDBottomAppBar.animation**

# TODO: add description.
# FIXME: changing the value does not affect anything.
Added in version 1.2.0.
[`animation`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar.animation) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivymd.uix.appbar.appbar.MDBottomAppBar.show_transition**

Type of button display transition.
Added in version 1.2.0.
[`show_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar.show_transition) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘linear’.

**kivymd.uix.appbar.appbar.MDBottomAppBar.hide_transition**

Type of button hidden transition.
Added in version 1.2.0.
[`hide_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar.hide_transition) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘in_back’.

**kivymd.uix.appbar.appbar.MDBottomAppBar.hide_duration**

Duration of button hidden transition.
Added in version 1.2.0.
[`hide_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar.hide_duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivymd.uix.appbar.appbar.MDBottomAppBar.show_duration**

Duration of button display transition.
Added in version 1.2.0.
[`show_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar.show_duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivymd.uix.appbar.appbar.MDBottomAppBar.scroll_cls**

Widget inherited from the [`ScrollView`](https://kivy.org/doc/stable/api-kivy.uix.scrollview.html#kivy.uix.scrollview.ScrollView) class.
The value must be set if the [`allow_hidden`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar.allow_hidden) parameter is True.
Added in version 1.2.0.
[`scroll_cls`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar.scroll_cls) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivymd.uix.appbar.appbar.MDBottomAppBar.allow_hidden**

Allows or disables hiding the panel when scrolling content.
If the value is True, the [`scroll_cls`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar.scroll_cls) parameter must be specified.
Added in version 1.2.0.
[`allow_hidden`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar.allow_hidden) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.appbar.appbar.MDBottomAppBar.bar_is_hidden**

Is the panel currently hidden.
Added in version 1.2.0.
[`bar_is_hidden`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar.bar_is_hidden) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.appbar.appbar.MDBottomAppBar.button_centering_animation**

Animation of centering buttons for
`MDActionOverFlowButton`,
[`MDActionBottomAppBarButton`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDActionBottomAppBarButton) and
[`MDFabBottomAppBarButton`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDFabBottomAppBarButton) classes.

**kivymd.uix.appbar.appbar.MDBottomAppBar.check_scroll_direction**

Checks the scrolling direction.
Depending on the scrolling direction, hides or shows the
[`MDBottomAppBar`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar) panel.

**kivymd.uix.appbar.appbar.MDBottomAppBar.show_bar**

Show [`MDBottomAppBar`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar) panel.

**kivymd.uix.appbar.appbar.MDBottomAppBar.hide_bar**

Hide [`MDBottomAppBar`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar) panel.

**kivymd.uix.appbar.appbar.MDBottomAppBar.on_show_bar**

The method is fired when the [`MDBottomAppBar`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar) panel
is shown.

**kivymd.uix.appbar.appbar.MDBottomAppBar.on_hide_bar**

The method is fired when the [`MDBottomAppBar`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar) panel
is hidden.

**kivymd.uix.appbar.appbar.MDBottomAppBar.on_scroll_cls**

Fired when the value of the [`scroll_cls`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar.scroll_cls) attribute changes.

**kivymd.uix.appbar.appbar.MDBottomAppBar.on_size**

Fired when the root screen is resized.

**kivymd.uix.appbar.appbar.MDBottomAppBar.on_action_items**

Fired when the value of the [`action_items`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDBottomAppBar.action_items) attribute changes.

**kivymd.uix.appbar.appbar.MDBottomAppBar.set_fab_opacity**

Sets the transparency value of the:class:~MDFabBottomAppBarButton
button.

**kivymd.uix.appbar.appbar.MDBottomAppBar.set_fab_icon**

Animates the size of the [`MDFabBottomAppBarButton`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.appbar.appbar.MDFabBottomAppBarButton) button.

**kivymd.uix.appbar.appbar.MDBottomAppBar.add_widget**

Add a new widget as a child of this widget.

---

## API - [`kivymd.uix.badge.badge`](https://kivymd.readthedocs.io/en/latest/components/badge/)

**kivymd.uix.badge.badge.MDBadge**

Badge class.
Added in version 2.0.0.
For more information see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) class documentation.

---

## API - [`kivymd.uix.bottomsheet.bottomsheet`](https://kivymd.readthedocs.io/en/latest/components/bottomsheet/)

**kivymd.uix.bottomsheet.bottomsheet.MDBottomSheetDragHandleButton**

Implements a close button (or other functionality) for the
[`MDBottomSheetDragHandle`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.bottomsheet.bottomsheet.MDBottomSheetDragHandle) container.
For more information, see in the
[`MDIconButton`](https://kivymd.readthedocs.io/en/button/#kivymd.uix.button.button.MDIconButton) class documentation.
Added in version 1.2.0.

**kivymd.uix.bottomsheet.bottomsheet.MDBottomSheetDragHandleTitle**

Implements a header for the [`MDBottomSheetDragHandle`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.bottomsheet.bottomsheet.MDBottomSheetDragHandle) container.
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) class documentation.
Added in version 1.2.0.

**kivymd.uix.bottomsheet.bottomsheet.MDBottomSheetDragHandle**

Implements a container that can place the header of the bottom sheet
and the close button. Also implements the event of dragging the
bottom sheet on the parent screen.
For more information, see in the
`DeclarativeBehavior` and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout) classes documentation.
Added in version 1.2.0.

**kivymd.uix.bottomsheet.bottomsheet.MDBottomSheetDragHandle.drag_handle_color**

Color of drag handle element in (r, g, b, a) or string format.

[`drag_handle_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.bottomsheet.bottomsheet.MDBottomSheetDragHandle.drag_handle_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.bottomsheet.bottomsheet.MDBottomSheetDragHandle.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.bottomsheet.bottomsheet.MDBottomSheet**

Bottom sheet class.
For more information, see in the
[`MDNavigationDrawer`](https://kivymd.readthedocs.io/en/navigationdrawer/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer)
class documentation.

**kivymd.uix.bottomsheet.bottomsheet.MDBottomSheet.sheet_type**

Type of sheet.
Standard bottom sheets co-exist with the screen’s main UI region and allow
for simultaneously viewing and interacting with both regions, especially
when the main UI region is frequently scrolled or panned. Use a standard
bottom sheet to display content that complements the screen’s primary
content, such as an audio player in a music app.
Like dialogs, modal bottom sheets appear in front of app content,
disabling all other app functionality when they appear, and remaining on
screen until confirmed, dismissed, or a required action has been taken.
Changed in version 2.0.0:Rename from type to sheet_type.
[`sheet_type`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.bottomsheet.bottomsheet.MDBottomSheet.sheet_type) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘modal’.

**kivymd.uix.bottomsheet.bottomsheet.MDBottomSheet.on_sheet_type**

Fired when the [`sheet_type`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.bottomsheet.bottomsheet.MDBottomSheet.sheet_type) value changes.

**kivymd.uix.bottomsheet.bottomsheet.MDBottomSheet.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.bottomsheet.bottomsheet.MDBottomSheet.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See `on_touch_down()` for more information.

---

## API - [`kivymd.uix.boxlayout`](https://kivymd.readthedocs.io/en/latest/components/boxlayout/)

**kivymd.uix.boxlayout.MDBoxLayout**

Box layout class.
For more information see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout) and
[`MDAdaptiveWidget`](https://kivymd.readthedocs.io/api/kivymd/uix/#kivymd.uix.MDAdaptiveWidget)
classes documentation.

---

## API - [`kivymd.uix.button.button`](https://kivymd.readthedocs.io/en/latest/components/button/)

**kivymd.uix.button.button.BaseFabButton**

Implements the basic properties for the
[`MDExtendedFabButton`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.MDExtendedFabButton) and [`MDFabButton`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.MDFabButton) classes.
Added in version 2.0.0.

**kivymd.uix.button.button.BaseFabButton.elevation_levels**

Elevation is measured as the distance between components along the z-axis
in density-independent pixels (dps).
Added in version 1.2.0.
[`elevation_levels`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseFabButton.elevation_levels) is an [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty)
and defaults to {0: dp(0), 1: dp(4), 2: dp(8), 3: dp(12), 4: dp(16), 5: dp(18)}.

**kivymd.uix.button.button.BaseFabButton.color_map**

Additional color mappings.
Available options are: ‘surface’, ‘secondary’, ‘tertiary’.
[`color_map`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseFabButton.color_map) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘secondary’.

**kivymd.uix.button.button.BaseFabButton.icon_color_disabled**

The icon color in (r, g, b, a) or string format of the list item when
the widget item is disabled.
[`icon_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseFabButton.icon_color_disabled) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.button.button.BaseFabButton.style**

Button type.
Available options are: ‘standard’, ‘small’, ‘large’.
[`style`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseFabButton.style) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘standard’.

**kivymd.uix.button.button.BaseFabButton.fab_state**

The state of the button.
Available options are: ‘collapse’ or ‘expand’.
[`fab_state`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseFabButton.fab_state) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to “collapse”.

**kivymd.uix.button.button.BaseFabButton.md_bg_color_disabled**

The background color in (r, g, b, a) or string format of the list item when
the list button is disabled.
[`md_bg_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseFabButton.md_bg_color_disabled) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.button.button.BaseFabButton.radius**

Canvas radius.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseFabButton.radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [dp(16), dp(16), dp(16), dp(16)].

**kivymd.uix.button.button.BaseButton**

Base button class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`RectangularRippleBehavior`](https://kivymd.readthedocs.io/behaviors/ripple/#id0) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`StateLayerBehavior`](https://kivymd.readthedocs.io/behaviors/state-layer/#kivymd.uix.behaviors.state_layer_behavior.StateLayerBehavior)
classes documentation.

**kivymd.uix.button.button.BaseButton.elevation_levels**

Elevation is measured as the distance between components along the z-axis
in density-independent pixels (dps).
Added in version 1.2.0.
[`elevation_levels`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseButton.elevation_levels) is an [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty)
and defaults to {0: dp(0), 1: dp(4), 2: dp(8), 3: dp(12), 4: dp(16), 5: dp(18)}.

**kivymd.uix.button.button.BaseButton.md_bg_color_disabled**

The background color in (r, g, b, a) or string format of the button when
the button is disabled.
[`md_bg_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseButton.md_bg_color_disabled) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.button.button.BaseButton.shadow_radius**

Button shadow radius.
[`shadow_radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseButton.shadow_radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [0, 0, 0, 0].

**kivymd.uix.button.button.BaseButton.md_bg_color**

Button background color in (r, g, b, a) or string format.
[`md_bg_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseButton.md_bg_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.button.button.BaseButton.line_color**

Outlined color.
[`line_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseButton.line_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.button.button.BaseButton.line_width**

Line width for button border.
[`line_width`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseButton.line_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 1.

**kivymd.uix.button.button.BaseButton.on_press**

Fired when the button is pressed.

**kivymd.uix.button.button.BaseButton.on_release**

Fired when the button is released
(i.e. the touch/click that pressed the button goes away).

**kivymd.uix.button.button.BaseButton.on_touch_down**

**kivymd.uix.button.button.BaseButton.finish_ripple**

**kivymd.uix.button.button.MDButton**

Base class for all buttons.
Added in version 2.2.0.
For more information, see in the
[`CommonElevationBehavior`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior) and
[`BaseButton`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseButton) and
[`RelativeLayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#kivy.uix.relativelayout.RelativeLayout)
classes documentation.

**kivymd.uix.button.button.MDButton.style**

Button type.
Available options are: ‘filled’, ‘elevated’, ‘outlined’, ‘tonal’, ‘text’.
[`style`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.MDButton.style) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘elevated’.

**kivymd.uix.button.button.MDButton.radius**

Button radius.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.MDButton.radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [dp(20), dp(20), dp(20), dp(20)].

**kivymd.uix.button.button.MDButton.adjust_pos**

Adjusts the pos of the button according to the content.

**kivymd.uix.button.button.MDButton.adjust_width**

Adjusts the width of the button according to the content.

**kivymd.uix.button.button.MDButton.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.button.button.MDButton.set_properties_widget**

Fired on_release/on_press/on_enter/on_leave events.

**kivymd.uix.button.button.MDButton.on_disabled**

Fired when the disabled value changes.

**kivymd.uix.button.button.MDButtonText**

The class implements the text for the [`MDButton`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.MDButton) class.
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) class documentation.

**kivymd.uix.button.button.MDButtonIcon**

The class implements an icon for the [`MDButton`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.MDButton) class.
For more information, see in the
[`MDIcon`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDIcon) class documentation.

**kivymd.uix.button.button.MDIconButton**

Base class for icon buttons.
For more information, see in the
[`RectangularRippleBehavior`](https://kivymd.readthedocs.io/behaviors/ripple/#id0) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
`MDIcon`
classes documentation.

**kivymd.uix.button.button.MDIconButton.style**

Button type.
Added in version 2.0.0.
Available options are: ‘standard’, ‘filled’, ‘tonal’, ‘outlined’.
[`style`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.MDIconButton.style) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘standard’.

**kivymd.uix.button.button.MDIconButton.md_bg_color_disabled**

The background color in (r, g, b, a) or string format of the list item when
the list button is disabled.
[`md_bg_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.MDIconButton.md_bg_color_disabled) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.button.button.MDIconButton.on_line_color**

Fired when the values of `line_color` change.

**kivymd.uix.button.button.MDFabButton**

Base class for FAB buttons.
For more information, see in the
[`BaseFabButton`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseFabButton) and
[`CommonElevationBehavior`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior) and
[`RectangularRippleBehavior`](https://kivymd.readthedocs.io/behaviors/ripple/#id0) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
[`MDIcon`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDIcon)
classes documentation.

**kivymd.uix.button.button.MDFabButton.on_press**

Fired when the button is pressed.

**kivymd.uix.button.button.MDFabButton.on_release**

Fired when the button is released
(i.e. the touch/click that pressed the button goes away).

**kivymd.uix.button.button.MDFabButton.set_properties_widget**

Fired on_release/on_press/on_enter/on_leave events.

**kivymd.uix.button.button.MDExtendedFabButtonIcon**

Implements an icon for the [`MDExtendedFabButton`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.MDExtendedFabButton) class.
Added in version 2.0.0.

**kivymd.uix.button.button.MDExtendedFabButtonText**

Implements the text for the class [`MDExtendedFabButton`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.MDExtendedFabButton) class.
Added in version 2.0.0.

**kivymd.uix.button.button.MDExtendedFabButton**

Base class for Extended FAB buttons.
Added in version 2.0.0.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`MotionExtendedFabButtonBehavior`](https://kivymd.readthedocs.io/behaviors/motion/#kivymd.uix.behaviors.motion_behavior.MotionExtendedFabButtonBehavior) and
[`CommonElevationBehavior`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior) and
[`StateLayerBehavior`](https://kivymd.readthedocs.io/behaviors/state-layer/#kivymd.uix.behaviors.state_layer_behavior.StateLayerBehavior) and
[`BaseFabButton`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.BaseFabButton) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
[`RelativeLayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#kivy.uix.relativelayout.RelativeLayout)
classes documentation.

**kivymd.uix.button.button.MDExtendedFabButton.elevation_levels**

Elevation is measured as the distance between components along the z-axis
in density-independent pixels (dps).
Added in version 1.2.0.
[`elevation_levels`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.button.button.MDExtendedFabButton.elevation_levels) is an [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty)
and defaults to {0: dp(0), 1: dp(4), 2: dp(8), 3: dp(12), 4: dp(16), 5: dp(18)}.

**kivymd.uix.button.button.MDExtendedFabButton.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.button.button.MDExtendedFabButton.on_collapse**

Fired when the button is collapsed.

**kivymd.uix.button.button.MDExtendedFabButton.on_expand**

Fired when the button is expanded.

**kivymd.uix.button.button.MDExtendedFabButton.on_fab_state**

Fired when the `fab_state` value changes.

**kivymd.uix.button.button.MDExtendedFabButton.on__x**

---

## API - [`kivymd.uix.card.card`](https://kivymd.readthedocs.io/en/latest/components/card/)

**kivymd.uix.card.card.MDCard**

Card class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`MDAdaptiveWidget`](https://kivymd.readthedocs.io/api/kivymd/uix/#kivymd.uix.MDAdaptiveWidget) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`CommonElevationBehavior`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior) and
[`RectangularRippleBehavior`](https://kivymd.readthedocs.io/behaviors/ripple/#id0) and
[`StateLayerBehavior`](https://kivymd.readthedocs.io/behaviors/state-layer/#kivymd.uix.behaviors.state_layer_behavior.StateLayerBehavior) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout) and
classes documentation.

**kivymd.uix.card.card.MDCard.ripple_behavior**

Use ripple effect for card.
[`ripple_behavior`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCard.ripple_behavior) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.card.card.MDCard.radius**

Card radius by default.
Added in version 1.0.0.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCard.radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [dp(16), dp(16), dp(16), dp(16)].

**kivymd.uix.card.card.MDCard.style**

Card type.
Added in version 1.0.0.
Available options are: ‘filled’, ‘elevated’, ‘outlined’.
[`style`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCard.style) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to None.

**kivymd.uix.card.card.MDCard.md_bg_color_disabled**

The background color in (r, g, b, a) or string format of the card when
the card is disabled.
[`md_bg_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCard.md_bg_color_disabled) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.card.card.MDCard.on_press**

Fired when the button is pressed.

**kivymd.uix.card.card.MDCard.on_release**

Fired when the button is released
(i.e. the touch/click that pressed the button goes away).

**kivymd.uix.card.card.MDCard.on_ripple_behavior**

Fired when the [`ripple_behavior`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCard.ripple_behavior) value changes.

**kivymd.uix.card.card.MDCard.set_properties_widget**

Fired on_release/on_press/on_enter/on_leave events.

**kivymd.uix.card.card.MDCardSwipe**

Card swipe class.
For more information, see in the
[`MDRelativeLayout`](https://kivymd.readthedocs.io/en/relativelayout/#kivymd.uix.relativelayout.MDRelativeLayout) class documentation.

**kivymd.uix.card.card.MDCardSwipe.open_progress**

Percent of visible part of side panel. The percent is specified as a
floating point number in the range 0-1. 0.0 if panel is closed and 1.0 if
panel is opened.
[`open_progress`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.open_progress) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.0.

**kivymd.uix.card.card.MDCardSwipe.opening_transition**

The name of the animation transition type to use when animating to
the [`state`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.state) ‘opened’.
[`opening_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.opening_transition) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘out_cubic’.

**kivymd.uix.card.card.MDCardSwipe.closing_transition**

The name of the animation transition type to use when animating to
the [`state`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.state) ‘closed’.
[`closing_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.closing_transition) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘out_sine’.

**kivymd.uix.card.card.MDCardSwipe.closing_interval**

Interval for closing the front layer.
Added in version 1.1.0.
[`closing_interval`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.closing_interval) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivymd.uix.card.card.MDCardSwipe.anchor**

Anchoring screen edge for card. Available options are: ‘left’, ‘right’.
[`anchor`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.anchor) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to left.

**kivymd.uix.card.card.MDCardSwipe.swipe_distance**

The distance of the swipe with which the movement of navigation drawer
begins.
[`swipe_distance`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.swipe_distance) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 50.

**kivymd.uix.card.card.MDCardSwipe.opening_time**

The time taken for the card to slide to the [`state`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.state) ‘open’.
[`opening_time`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.opening_time) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivymd.uix.card.card.MDCardSwipe.state**

Detailed state. Sets before [`state`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.state). Bind to [`state`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.state) instead
of `status`. Available options are: ‘closed’, ‘opened’.
`status` is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘closed’.

**kivymd.uix.card.card.MDCardSwipe.max_swipe_x**

If, after the events of [`on_touch_up`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.on_touch_up) card position exceeds this
value - will automatically execute the method [`open_card`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.open_card),
and if not - will automatically be [`close_card`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.close_card) method.
[`max_swipe_x`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.max_swipe_x) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.3.

**kivymd.uix.card.card.MDCardSwipe.max_opened_x**

The value of the position the card shifts to when [`type_swipe`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.type_swipe)
s set to ‘hand’.
[`max_opened_x`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.max_opened_x) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 100dp.

**kivymd.uix.card.card.MDCardSwipe.type_swipe**

Type of card opening when swipe. Shift the card to the edge or to
a set position [`max_opened_x`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.max_opened_x). Available options are:
‘auto’, ‘hand’.
[`type_swipe`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.type_swipe) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to auto.

**kivymd.uix.card.card.MDCardSwipe.on_swipe_complete**

Fired when a swipe of card is completed.

**kivymd.uix.card.card.MDCardSwipe.on_anchor**

Fired when the value of [`anchor`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.anchor) changes.

**kivymd.uix.card.card.MDCardSwipe.on_open_progress**

Fired when the value of [`open_progress`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.open_progress) changes.

**kivymd.uix.card.card.MDCardSwipe.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.on_touch_down) for more information.

**kivymd.uix.card.card.MDCardSwipe.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCardSwipe.on_touch_down) for more information.

**kivymd.uix.card.card.MDCardSwipe.on_touch_down**

Receive a touch down event.

**kivymd.uix.card.card.MDCardSwipe.open_card**

Animates the opening of the card.

**kivymd.uix.card.card.MDCardSwipe.close_card**

Animates the closing of the card.

**kivymd.uix.card.card.MDCardSwipe.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.card.card.MDCardSwipeFrontBox**

Card swipe front box.
For more information, see in the [`MDCard`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.card.card.MDCard) class documentation.

**kivymd.uix.card.card.MDCardSwipeLayerBox**

Card swipe back box.
For more information, see in the [`MDBoxLayout`](https://kivymd.readthedocs.io/en/boxlayout/#kivymd.uix.boxlayout.MDBoxLayout)
class documentation.

---

## API - [`kivymd.uix.carousel.carousel`](https://kivymd.readthedocs.io/en/latest/components/carousel/)

**kivymd.uix.carousel.carousel.MDCarouselItem**

Implements a item for [`MDCarousel`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.carousel.carousel.MDCarousel) class.
For more information, see in the [`MDCard`](https://kivymd.readthedocs.io/en/card/#kivymd.uix.card.card.MDCard)
class documentation.

**kivymd.uix.carousel.carousel.MDCarouselItem.full_screen_radius**

Corner radius used during scrolling for items in full-screen layout modes.

[`full_screen_radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.carousel.carousel.MDCarouselItem.full_screen_radius) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to dp(16).

**kivymd.uix.carousel.carousel.MDCarouselItem.radius**

Item radius by default.

[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.carousel.carousel.MDCarouselItem.radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [dp(28), dp(28), dp(28), dp(28)].

**kivymd.uix.carousel.carousel.MDCarouselItem.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.carousel.carousel.MDCarousel**

Implements a custom Material Design 3 carousel.
For more information, see in the `MDWidget`
class documentation.

**kivymd.uix.carousel.carousel.MDCarousel.padding**

Padding of the carousel view in the format `[left, top, right, bottom]`.
[`padding`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.carousel.carousel.MDCarousel.padding) is an [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to `[dp(16), dp(16), dp(16), dp(16)]`.

**kivymd.uix.carousel.carousel.MDCarousel.spacing**

Distance between items in the carousel.
[`spacing`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.carousel.carousel.MDCarousel.spacing) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to `dp(12)`.

**kivymd.uix.carousel.carousel.MDCarousel.shrink_extent**

Size of the collapsed or shrinked extent for trailing items.
[`shrink_extent`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.carousel.carousel.MDCarousel.shrink_extent) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to `dp(56)`.

**kivymd.uix.carousel.carousel.MDCarousel.item_snapping**

If `True`, enables automatic snapping of items to the closest slot upon touch release.
[`item_snapping`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.carousel.carousel.MDCarousel.item_snapping) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to `True`.

**kivymd.uix.carousel.carousel.MDCarousel.scroll_offset**

Current scroll offset value of the carousel.
[`scroll_offset`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.carousel.carousel.MDCarousel.scroll_offset) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to `0`.

**kivymd.uix.carousel.carousel.MDCarousel.layouts**

Layout type of the carousel view.
Available options are:
- `"multi-browse"`: Standard layout displaying multiple items of varying sizes.
- `"uncontained"`: Items maintain a fixed width and overflow beyond the carousel edge.
- `"hero"`: Highlights a single large hero item aligned to the start.
- `"center-aligned"`: Displays a centered hero item flanked by smaller preview items.
- `"full-screen-horizontal"`: Items occupy the full width and height of the carousel, scrolling horizontally.
- `"full-screen-vertical"`: Items occupy the full width and height of the carousel, scrolling vertically.
[`layouts`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.carousel.carousel.MDCarousel.layouts) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to `"multi-browse"`.
Multi-browse[#](https://kivymd.readthedocs.io/en/latest/#multi-browse)
Uncontained[#](https://kivymd.readthedocs.io/en/latest/#uncontained)
Hero[#](https://kivymd.readthedocs.io/en/latest/#hero)
Center-aligned[#](https://kivymd.readthedocs.io/en/latest/#center-aligned)
Full-screen-vertical[#](https://kivymd.readthedocs.io/en/latest/#full-screen-vertical)

[](https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/carousel-full-screen-vertical.gif)
Full-screen-horizontal[#](https://kivymd.readthedocs.io/en/latest/#full-screen-horizontal)

[](https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/carousel-full-screen-horizontal.gif)

**kivymd.uix.carousel.carousel.MDCarousel.uncontained_item_width**

Width of individual items when using the `"uncontained"` layout mode.
[`uncontained_item_width`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.carousel.carousel.MDCarousel.uncontained_item_width) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to `dp(280)`.

**kivymd.uix.carousel.carousel.MDCarousel.index**

Index of the currently active item.
[`index`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.carousel.carousel.MDCarousel.index) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to `0`.

**kivymd.uix.carousel.carousel.MDCarousel.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.carousel.carousel.MDCarousel.on_touch_down**

Receive a touch down event.

**kivymd.uix.carousel.carousel.MDCarousel.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.carousel.carousel.MDCarousel.on_touch_down) for more information.

**kivymd.uix.carousel.carousel.MDCarousel.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.carousel.carousel.MDCarousel.on_touch_down) for more information.

**kivymd.uix.carousel.carousel.MDCarousel.on_index**

Fired when the active slide index changes.

**kivymd.uix.carousel.carousel.MDCarousel.on_slide_left**

Fired when user slides/swipes to the left.

**kivymd.uix.carousel.carousel.MDCarousel.on_slide_right**

Fired when user slides/swipes to the right.

**kivymd.uix.carousel.carousel.MDCarousel.on_slide_up**

Fired when user slides/swipes up.

**kivymd.uix.carousel.carousel.MDCarousel.on_slide_down**

Fired when user slides/swipes down.

---

## API - [`kivymd.uix.chip.chip`](https://kivymd.readthedocs.io/en/latest/components/chip/)

**kivymd.uix.chip.chip.MDChipLeadingAvatar**

Implements the leading avatar for the chip.
For more information, see in the
[`CircularRippleBehavior`](https://kivymd.readthedocs.io/behaviors/ripple/#id1) and
[`ScaleBehavior`](https://kivymd.readthedocs.io/behaviors/scale/#kivymd.uix.behaviors.scale_behavior.ScaleBehavior) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
[`MDIcon`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDIcon)
classes documentation.

**kivymd.uix.chip.chip.MDChipLeadingIcon**

Implements the leading icon for the chip.
For more information, see in the
[`CircularRippleBehavior`](https://kivymd.readthedocs.io/behaviors/ripple/#id1) and
[`ScaleBehavior`](https://kivymd.readthedocs.io/behaviors/scale/#kivymd.uix.behaviors.scale_behavior.ScaleBehavior) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
[`MDIcon`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDIcon)
classes documentation.

**kivymd.uix.chip.chip.MDChipTrailingIcon**

Implements the trailing icon for the chip.
For more information, see in the
[`CircularRippleBehavior`](https://kivymd.readthedocs.io/behaviors/ripple/#id1) and
[`ScaleBehavior`](https://kivymd.readthedocs.io/behaviors/scale/#kivymd.uix.behaviors.scale_behavior.ScaleBehavior) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
[`MDIcon`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDIcon)
classes documentation.

**kivymd.uix.chip.chip.MDChipText**

Implements the label for the chip.
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) classes documentation.

**kivymd.uix.chip.chip.MDChipText.text_color_disabled**

The text color in (r, g, b, a) or string format of the chip when
the chip is disabled.
Added in version 2.0.0.
[`text_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.chip.chip.MDChipText.text_color_disabled) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.chip.chip.MDChip**

Chip class.
For more information, see in the
[`MDBoxLayout`](https://kivymd.readthedocs.io/en/boxlayout/#kivymd.uix.boxlayout.MDBoxLayout) and
[`RectangularRippleBehavior`](https://kivymd.readthedocs.io/behaviors/ripple/#id0) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
[`CommonElevationBehavior`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior) and
[`TouchBehavior`](https://kivymd.readthedocs.io/behaviors/touch/#kivymd.uix.behaviors.touch_behavior.TouchBehavior)
classes documentation.

**kivymd.uix.chip.chip.MDChip.radius**

Chip radius.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.chip.chip.MDChip.radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [dp(8), dp(8), dp(8), dp(8)].

**kivymd.uix.chip.chip.MDChip.type**

Type of chip.
Added in version 2.0.0.
Available options are: ‘assist’, ‘filter’, ‘input’, ‘suggestion’.
[`type`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.chip.chip.MDChip.type) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘suggestion’.

**kivymd.uix.chip.chip.MDChip.active**

Whether the check is marked or not.
Added in version 1.0.0.
[`active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.chip.chip.MDChip.active) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.chip.chip.MDChip.selected_color**

The background color of the chip in the marked state in (r, g, b, a)
or string format.
Added in version 2.0.0.
[`selected_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.chip.chip.MDChip.selected_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.chip.chip.MDChip.line_color_disabled**

The color of the outline in the disabled state
Added in version 2.0.0.
[`line_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.chip.chip.MDChip.line_color_disabled) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.chip.chip.MDChip.on_long_touch**

Fired when the widget is pressed for a long time.

**kivymd.uix.chip.chip.MDChip.on_line_color**

Fired when the values of `line_color` change.

**kivymd.uix.chip.chip.MDChip.on_type**

Fired when the values of [`type`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.chip.chip.MDChip.type) change.

**kivymd.uix.chip.chip.MDChip.on_active**

Called when the values of [`active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.chip.chip.MDChip.active) change.

**kivymd.uix.chip.chip.MDChip.complete_anim_ripple**

Called at the end of the ripple animation.

**kivymd.uix.chip.chip.MDChip.remove_marked_icon_from_chip**

**kivymd.uix.chip.chip.MDChip.add_marked_icon_to_chip**

Adds and animates a check icon to the chip.

**kivymd.uix.chip.chip.MDChip.set_chip_bg_color**

Animates the background color of the chip.

**kivymd.uix.chip.chip.MDChip.on_press**

Fired when the button is pressed.

**kivymd.uix.chip.chip.MDChip.on_release**

Fired when the button is released
(i.e. the touch/click that pressed the button goes away).

**kivymd.uix.chip.chip.MDChip.add_widget**

Add a new widget as a child of this widget.

---

## API - [`kivymd.uix.circularlayout`](https://kivymd.readthedocs.io/en/latest/components/circularlayout/)

**kivymd.uix.circularlayout.MDCircularLayout**

Circular layout class.
For more information see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`FloatLayout`](https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html#kivy.uix.floatlayout.FloatLayout)
classes documentation.

**kivymd.uix.circularlayout.MDCircularLayout.degree_spacing**

The space between children in degree.
[`degree_spacing`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.circularlayout.MDCircularLayout.degree_spacing) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 30.

**kivymd.uix.circularlayout.MDCircularLayout.circular_radius**

Radius of circle. Radius will be the greatest value in the layout
if circular_radius if not specified.
[`circular_radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.circularlayout.MDCircularLayout.circular_radius) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to None.

**kivymd.uix.circularlayout.MDCircularLayout.start_from**

The positon of first child in degree.
[`start_from`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.circularlayout.MDCircularLayout.start_from) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 60.

**kivymd.uix.circularlayout.MDCircularLayout.max_degree**

Maximum range in degree allowed for each row of widgets before jumping
to the next row.
[`max_degree`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.circularlayout.MDCircularLayout.max_degree) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 360.

**kivymd.uix.circularlayout.MDCircularLayout.circular_padding**

Padding between outer widgets and the edge of the biggest circle.
[`circular_padding`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.circularlayout.MDCircularLayout.circular_padding) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 25dp.

**kivymd.uix.circularlayout.MDCircularLayout.row_spacing**

Space between each row of widget.
[`row_spacing`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.circularlayout.MDCircularLayout.row_spacing) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 50dp.

**kivymd.uix.circularlayout.MDCircularLayout.clockwise**

Direction of widgets in circular direction.
[`clockwise`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.circularlayout.MDCircularLayout.clockwise) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivymd.uix.circularlayout.MDCircularLayout.get_angle**

Returns the angle of given pos.

**kivymd.uix.circularlayout.MDCircularLayout.remove_widget**

Remove a widget from the children of this widget.

**kivymd.uix.circularlayout.MDCircularLayout.do_layout**

This function is called when a layout is called by a trigger.
If you are writing a new Layout subclass, don’t call this function
directly but use `_trigger_layout()` instead.
The function is by default called *before* the next frame, therefore
the layout isn’t updated immediately. Anything depending on the
positions of e.g. children should be scheduled for the next frame.
Added in version 1.0.8.

---

## API - [`kivymd.uix.datatables.datatables`](https://kivymd.readthedocs.io/en/latest/components/datatables/)

**kivymd.uix.datatables.datatables.MDDataTable**

Datatable class.
For more information, see in the
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`AnchorLayout`](https://kivy.org/doc/stable/api-kivy.uix.anchorlayout.html#kivy.uix.anchorlayout.AnchorLayout) classes documentation.

Use events as follows

**kivymd.uix.datatables.datatables.MDDataTable.column_data**

Data for header columns.
Imperative python styleDeclarative python style

[`column_data`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.column_data) is an [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [].

**kivymd.uix.datatables.datatables.MDDataTable.row_data**

Data for rows. To add icon in addition to a row data, include a tuple with
This property stores the row data used to display each row in the DataTable
To show an icon inside a column in a row, use the folowing format in the
row’s columns.
Format:
(“MDicon-name”, [icon color in rgba], “Column Value”)
Example:

For a more complex example see below.

Custom widgets in cells.

Custom widgets with children in cells.

[`row_data`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.row_data) is an [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [].

**kivymd.uix.datatables.datatables.MDDataTable.sorted_on**

Column name upon which the data is already sorted.
If the table data is showing an already sorted data then this can be used
to indicate upon which column the data is sorted.
[`sorted_on`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.sorted_on) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘’.

**kivymd.uix.datatables.datatables.MDDataTable.sorted_order**

Order of already sorted data. Must be one of ‘ASC’ for ascending or
‘DSC’ for descending order.
[`sorted_order`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.sorted_order) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘ASC’.

**kivymd.uix.datatables.datatables.MDDataTable.check**

Use or not use checkboxes for rows.

[`check`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.check) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.datatables.datatables.MDDataTable.use_pagination**

Use page pagination for table or not.

[`use_pagination`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.use_pagination) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.datatables.datatables.MDDataTable.radius**

See [`kivymd.uix.behaviors.elevation.CommonElevationBehavior.shadow_radius`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior.shadow_radius)
attribute.
Added in version 1.2.0.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [dp(6), dp(6), dp(6), dp(6)].

**kivymd.uix.datatables.datatables.MDDataTable.rows_num**

The number of rows displayed on one page of the table.

[`rows_num`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.rows_num) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 10.

**kivymd.uix.datatables.datatables.MDDataTable.pagination_menu_pos**

Menu position for selecting the number of displayed rows.
Available options are ‘center’, ‘auto’.
Center

Auto

[`pagination_menu_pos`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.pagination_menu_pos) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘center’.

**kivymd.uix.datatables.datatables.MDDataTable.pagination_menu_height**

Menu height for selecting the number of displayed rows.
240dp

[`pagination_menu_height`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.pagination_menu_height) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to ‘140dp’.

**kivymd.uix.datatables.datatables.MDDataTable.background_color**

Background color in the format (r, g, b, a) or string format.
See [`background_color`](https://kivy.org/doc/stable/api-kivy.uix.modalview.html#kivy.uix.modalview.ModalView.background_color).
Use markup strings[#](https://kivymd.readthedocs.io/en/latest/#use-markup-strings)

[`background_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.background_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to None.

**kivymd.uix.datatables.datatables.MDDataTable.background_color_header**

Background color in the format (r, g, b, a) or string format for
`TableHeader` class.
Added in version 1.0.0.

[`background_color_header`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.background_color_header) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to None.

**kivymd.uix.datatables.datatables.MDDataTable.background_color_cell**

Background color in the format (r, g, b, a) or string format for
`CellRow` class.
Added in version 1.0.0.

[`background_color_cell`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.background_color_cell) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.datatables.datatables.MDDataTable.background_color_selected_cell**

Background selected color in the format (r, g, b, a) or string format for
`CellRow` class.
Added in version 1.0.0.

[`background_color_selected_cell`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.background_color_selected_cell) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to None.

**kivymd.uix.datatables.datatables.MDDataTable.effect_cls**

Effect class. See `kivy/effects` package for more information.
Added in version 1.0.0.
[`effect_cls`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.effect_cls) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to `StiffScrollEffect`.

**kivymd.uix.datatables.datatables.MDDataTable.set_row_checked**

Sets the checkbox state for a specific row by its index.
Added in version 2.0.0.

You can select multiple rows at once:

Or toggle the selected row:

**kivymd.uix.datatables.datatables.MDDataTable.set_rows_checked**

Sets the checkbox state for multiple rows.
Added in version 2.0.0.

**kivymd.uix.datatables.datatables.MDDataTable.set_all_rows_checked**

Sets the state of all checkboxes in the table.

**kivymd.uix.datatables.datatables.MDDataTable.toggle_row_checked**

Toggles the checkbox state for a specific row.
Added in version 2.0.0.

**kivymd.uix.datatables.datatables.MDDataTable.is_row_checked**

Checks if a specific row is checked.
Added in version 2.0.0.

**kivymd.uix.datatables.datatables.MDDataTable.get_checked_row_indices**

Returns a list of indices of all checked rows.

**kivymd.uix.datatables.datatables.MDDataTable.clear_all_checks**

Unchecks all rows in the table.

**kivymd.uix.datatables.datatables.MDDataTable.check_all_rows**

Checks all rows in the table.

**kivymd.uix.datatables.datatables.MDDataTable.update_row_data**

Called when a the widget data must be updated.
Remember that this is a heavy function. since the whole data set must
be updated. you can get better results calling this metod with in a
coroutine.

**kivymd.uix.datatables.datatables.MDDataTable.add_row**

Added new row to common table.
Argument data is the row data from the list [`row_data`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.row_data).
Add/remove row

Deleting checked rows[#](https://kivymd.readthedocs.io/en/latest/#deleting-checked-rows)

Added in version 1.0.0.

**kivymd.uix.datatables.datatables.MDDataTable.remove_row**

Removed row from common table.
Argument data is the row data from the list [`row_data`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.row_data).
See the code in the doc string for the [`add_row`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.add_row) method for more
information.
Added in version 1.0.0.

**kivymd.uix.datatables.datatables.MDDataTable.update_row**

Updates a table row.
Argument old_data/new_data is the row data from the list [`row_data`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.datatables.datatables.MDDataTable.row_data).
Update row

Added in version 1.0.0.

**kivymd.uix.datatables.datatables.MDDataTable.on_row_press**

Called when a table row is clicked.

**kivymd.uix.datatables.datatables.MDDataTable.on_check_press**

Called when the check box in the table row is checked.

**kivymd.uix.datatables.datatables.MDDataTable.get_row_checks**

Returns all rows that are checked.

**kivymd.uix.datatables.datatables.MDDataTable.create_pagination_menu**

---

## API - [`kivymd.uix.dialog.dialog`](https://kivymd.readthedocs.io/en/latest/components/dialog/)

**kivymd.uix.dialog.dialog.MDDialog**

Dialog class.
For more information, see in the
[`MDCard`](https://kivymd.readthedocs.io/en/card/#kivymd.uix.card.card.MDCard) and
[`MotionDialogBehavior`](https://kivymd.readthedocs.io/behaviors/motion/#kivymd.uix.behaviors.motion_behavior.MotionDialogBehavior)
classes documentation.

**kivymd.uix.dialog.dialog.MDDialog.width_offset**

Dialog offset from device width.
[`width_offset`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.dialog.dialog.MDDialog.width_offset) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to dp(48).

**kivymd.uix.dialog.dialog.MDDialog.radius**

Dialog corners rounding value.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.dialog.dialog.MDDialog.radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [dp(28), dp(28), dp(28), dp(28)].

**kivymd.uix.dialog.dialog.MDDialog.scrim_color**

Color for scrim in (r, g, b, a) or string format.
[`scrim_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.dialog.dialog.MDDialog.scrim_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to [0, 0, 0, 0.5].

**kivymd.uix.dialog.dialog.MDDialog.auto_dismiss**

This property determines if the dialog is automatically
dismissed when the user clicks outside it.
..versionadded:: 2.0.0
[`auto_dismiss`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.dialog.dialog.MDDialog.auto_dismiss) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivymd.uix.dialog.dialog.MDDialog.update_width**

Fired when the application window is resized.

**kivymd.uix.dialog.dialog.MDDialog.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.dialog.dialog.MDDialog.set_properties_widget**

Fired on_release/on_press/on_enter/on_leave events.

**kivymd.uix.dialog.dialog.MDDialog.open**

Show the dialog.

**kivymd.uix.dialog.dialog.MDDialog.on_pre_open**

Fired when a dialog pre opened.

**kivymd.uix.dialog.dialog.MDDialog.on_open**

Fired when a dialog opened.

**kivymd.uix.dialog.dialog.MDDialog.on_dismiss**

Fired when a dialog dismiss.

**kivymd.uix.dialog.dialog.MDDialog.on_pre_dismiss**

Fired when a dialog pre-dismiss.

**kivymd.uix.dialog.dialog.MDDialog.on_touch_down**

Receive a touch down event.

**kivymd.uix.dialog.dialog.MDDialog.dismiss**

Closes the dialog.

**kivymd.uix.dialog.dialog.MDDialogIcon**

The class implements an icon.
For more information, see in the
[`MDIcon`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDIcon) class documentation.

**kivymd.uix.dialog.dialog.MDDialogHeadlineText**

The class implements the headline text.
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) class documentation.

**kivymd.uix.dialog.dialog.MDDialogSupportingText**

The class implements the supporting text.
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) class documentation.

**kivymd.uix.dialog.dialog.MDDialogContentContainer**

The class implements the container for custom widgets.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout) classes documentation.

**kivymd.uix.dialog.dialog.MDDialogButtonContainer**

The class implements a container for placing dialog buttons.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout) classes documentation.

---

## API - [`kivymd.uix.divider.divider`](https://kivymd.readthedocs.io/en/latest/components/divider/)

**kivymd.uix.divider.divider.MDDivider**

A divider line.
Added in version 2.0.0.
For more information, see in the
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout) classes documentation.

**kivymd.uix.divider.divider.MDDivider.color**

Divider color in (r, g, b, a) or string format.
[`color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.divider.divider.MDDivider.color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.divider.divider.MDDivider.divider_width**

Divider width.
[`divider_width`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.divider.divider.MDDivider.divider_width) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to dp(1).

**kivymd.uix.divider.divider.MDDivider.on_orientation**

Fired when the values of `orientation` change.

---

## API - [`kivymd.uix.dropdownitem.dropdownitem`](https://kivymd.readthedocs.io/en/latest/components/dropdownitem/)

**kivymd.uix.dropdownitem.dropdownitem.MDDropDownItemText**

Base texture for [`MDDropDownItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.dropdownitem.dropdownitem.MDDropDownItem) class (item text).
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) class documentation.
Added in version 2.0.0.

**kivymd.uix.dropdownitem.dropdownitem.MDDropDownItem**

Dropdown item class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
classes documentation.

**kivymd.uix.dropdownitem.dropdownitem.MDDropDownItem.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.dropdownitem.dropdownitem.MDDropDownItem.update_text_item**

Updates the text of the item.

**kivymd.uix.dropdownitem.dropdownitem.MDDropDownItem.on_disabled**

Fired when the values of `disabled` change.

**kivymd.uix.dropdownitem.dropdownitem.MDDropDownItem.on__drop_down_text**

Fired when the values of `_drop_down_text` change.

---

## API - [`kivymd.uix.expansionpanel.expansionpanel`](https://kivymd.readthedocs.io/en/latest/components/expansionpanel/)

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanelContent**

Implements a container for panel content.
Added in version 2.0.0.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
classes documentation.

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanelContent.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanelHeader**

Implements a container for the content of the panel header.
Added in version 2.0.0.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
classes documentation.

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel**

Expansion panel class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
classes documentation.

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.opening_transition**

The name of the animation transition type to use when animating to
the `state` ‘open’.
[`opening_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.opening_transition) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘out_cubic’.

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.opening_time**

The time taken for the panel to slide to the `state` ‘open’.
[`opening_time`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.opening_time) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.closing_transition**

The name of the animation transition type to use when animating to
the `state` ‘close’.
[`closing_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.closing_transition) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘out_sine’.

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.closing_time**

The time taken for the panel to slide to the `state` ‘close’.
[`closing_time`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.closing_time) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.is_open**

The panel is open or closed.
Added in version 2.0.0.
[`is_open`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.is_open) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.on_open**

Fired when a panel is opened.

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.on_close**

Fired when a panel is closed.

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.set_chevron_down**

Sets the chevron down.

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.set_chevron_up**

Sets the chevron up.

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.close**

Method closes the panel.
Changed in version 2.0.0:Rename from close_panel to close method.

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.open**

Method opens a panel.
Changed in version 2.0.0:Rename from open_panel to open method.

**kivymd.uix.expansionpanel.expansionpanel.MDExpansionPanel.add_widget**

Add a new widget as a child of this widget.

---

## API - [`kivymd.uix.exprogressindicator.animators`](https://kivymd.readthedocs.io/en/latest/api/kivymd/uix/exprogressindicator/animators/)

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateDisjointAnimator**

Animator for the Material Design linear indeterminate progress indicator
using the disjoint animation style.
The animation consists of two independent line segments whose head and tail
positions are animated with individual cubic Bézier interpolators.
Ported from the Android Material Components implementation
(LinearIndeterminateDisjointAnimatorDelegate).

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateDisjointAnimator.INTERPOLATORS**

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateDisjointAnimator.DURATION_TO_MOVE_SEGMENT_ENDS**

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateDisjointAnimator.DELAY_TO_MOVE_SEGMENT_ENDS**

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateDisjointAnimator.TOTAL_DURATION_IN_MS**

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateDisjointAnimator.LOOP_DELAY**

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateDisjointAnimator.get_fraction_in_range**

Returns the normalized animation fraction for the specified time range.

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateDisjointAnimator.compute_bar**

Computes the start and end positions of an animated line segment.

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateDisjointAnimator.bars**

Calculates the current state of the disjoint linear indicator.

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateContiguousAnimator**

Animator for the Material Design linear indeterminate progress indicator
using the contiguous animation style.
The progress indicator is divided into three connected segments that move
continuously across the track while cycling through the color palette.
Ported from the Android Material Components implementation
(LinearIndeterminateContiguousAnimatorDelegate).

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateContiguousAnimator.INTERPOLATOR**

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateContiguousAnimator.TOTAL_DURATION_IN_MS**

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateContiguousAnimator.DURATION_PER_CYCLE_IN_MS**

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateContiguousAnimator.last_cycle_count**

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateContiguousAnimator.current_indices**

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateContiguousAnimator.len_palette**

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateContiguousAnimator.get_fraction_in_range**

Returns the normalized animation fraction for the specified time range.

**kivymd.uix.exprogressindicator.animators.LinearIndeterminateContiguousAnimator.bars**

Calculates the current state of the contiguous linear indicator.

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateRetreatAnimator**

Animator for the Material Design circular indeterminate progress indicator
using the retreat animation style.
The animation continuously rotates the indicator while expanding and
shrinking the visible arc. The active color changes after each rotation
cycle.
Ported from the Android Material Components implementation
(CircularIndeterminateRetreatAnimatorDelegate).

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateRetreatAnimator.INTERPOLATOR**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateRetreatAnimator.TOTAL_DURATION_MS**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateRetreatAnimator.DURATION_SPIN_MS**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateRetreatAnimator.DURATION_GROW_MS**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateRetreatAnimator.DURATION_SHRINK_MS**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateRetreatAnimator.DELAY_SPINS_MS**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateRetreatAnimator.CONSTANT_ROTATION_DEGREES**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateRetreatAnimator.SPIN_ROTATION_DEGREES**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateRetreatAnimator.END_FRACTION_RANGE**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateRetreatAnimator.get_fraction_in_range**

Returns the normalized animation fraction for the specified time range.

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateRetreatAnimator.bars**

Calculates the current state of the retreat circular indicator.

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator**

Animator for the Material Design circular indeterminate progress indicator
using the advanced animation style.
The animation expands and collapses the arc while smoothly rotating around
the circle. Color transitions are synchronized with each animation cycle.
Ported from the Android Material Components implementation
(CircularIndeterminateAdvanceAnimatorDelegate).

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator.INTERPOLATOR**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator.TOTAL_DURATION_MS**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator.TOTAL_CYCLES**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator.DURATION_EXPAND**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator.DURATION_COLLAPSE**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator.DURATION_FADE_IN**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator.DELAY_EXPAND**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator.DELAY_COLLAPSE**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator.DELAY_FADE_IN**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator.TAIL_DEGREES_OFFSET**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator.EXTRA_DEGREES_PER_CYCLE**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator.CONSTANT_ROTATION_DEGREES**

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator.get_fraction_in_range**

Returns the normalized animation fraction for the specified time range.

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator.get_color**

Calculates the current color transition.

**kivymd.uix.exprogressindicator.animators.CircularIndeterminateAdvancedAnimator.bars**

Calculates the current state of the advanced circular indicator.

---

## API - [`kivymd.uix.exprogressindicator.exprogressindicator`](https://kivymd.readthedocs.io/en/latest/components/exprogressindicator/)

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar**

Base class for extended progress indicators.
Handles shared properties, frame context caching, and wave rendering hooks
used by both linear and circular indicators.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
classes documentation.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.value**

Current value used for the slider.
[`value`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.value) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) that
returns the value of the progress bar. If the value is < 0 or >
[`max`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.max), it will be normalized to those boundaries.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.value_normalized**

Normalized value inside the range 0-1:

[`value_normalized`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.value_normalized) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.max**

Maximum value allowed for [`value`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.value).
[`max`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.max) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to
100.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.active_track_color**

Color of active track
[`active_track_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.active_track_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and defaults to
None.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.inactive_track_color**

Color of inactive track
[`inactive_track_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.inactive_track_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and defaults to
None.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.thickness**

Thickness of tracks
[`thickness`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.thickness) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to dp(4).

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.spacing**

Spacing between tracks/segments.
[`spacing`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.spacing) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to dp(4).

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.amplitude**

Amplitude of the wave effect.
[`amplitude`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.amplitude) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to dp(3).

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.wave_speed**

Speed of the wave effect.
[`wave_speed`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.wave_speed) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to -dp(40) per second.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.wave_length**

Wavelength of the wave effect.
[`wave_length`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.wave_length) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to dp(40).

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.determinate**

Switch between determinate and indeterminate modes.
[`determinate`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.determinate) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.color_array**

List of RGBA colors used by indeterminate animations.
[`color_array`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.color_array) is an [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to three RGBA colors.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.get_norm_value**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.set_norm_value**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.color_obj**

Get color object from line.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.reset_colors**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.refresh_lines**

Clears points and returns a reusable queue.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.setup_lines**

init line objs

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.render_determinate_wave**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.render_indeterminate_wave**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.save_frame_context**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.on_determinate**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExBaseProgressBar.get_amplitude**

fade in/out for amplitude using quadratic easing.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator**

Implementation of the linear progress indicator.
For more information, see in the
`MDExBaseProgressBar` and
classes documentation.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.orientation**

Orientation of progressbar. Available options are: ‘horizontal ‘,
‘vertical’.
[`orientation`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.orientation) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘horizontal’.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.indeterminate_animator**

Name of the indeterminate animator to use for linear mode.
Available options are: ‘contiguous’, ‘discontinuous’.
[`indeterminate_animator`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.indeterminate_animator) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘discontinuous’.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.save_frame_context**

Pre-calculate geometry and spacing factors for the current frame.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.on_color_array**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.on_indeterminate_animator**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.on_orientation**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.w_seg**

High-performance wave point generator.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.cleanup_lines**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.compute_inactive_segments**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.render_determinate_wave**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.get_segment_coords**

Calculates points ensuring consistent visual gaps.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.render_discts_wave**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.render_cont_wave**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExLinearProgressIndicator.render_indeterminate_wave**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExCircularProgressIndicator**

Implementation of the circular progress indicator.
For more information, see in the
`MDExBaseProgressBar` and
classes documentation.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExCircularProgressIndicator.indeterminate_animator**

Name of the indeterminate animator to use for circular mode.
Available options are: ‘advanced’, ‘retreat’.
[`indeterminate_animator`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExCircularProgressIndicator.indeterminate_animator) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘retreat’.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExCircularProgressIndicator.use_color_array**

Whether to use `color_array` for circular active track colors.
[`use_color_array`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.exprogressindicator.exprogressindicator.MDExCircularProgressIndicator.use_color_array) is an
[`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to True.

**kivymd.uix.exprogressindicator.exprogressindicator.MDExCircularProgressIndicator.on_color_array**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExCircularProgressIndicator.save_frame_context**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExCircularProgressIndicator.w_seg**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExCircularProgressIndicator.get_arc_points**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExCircularProgressIndicator.get_start_and_end**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExCircularProgressIndicator.render_retreat_wave**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExCircularProgressIndicator.render_indeterminate_wave**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExCircularProgressIndicator.render_advanced_wave**

**kivymd.uix.exprogressindicator.exprogressindicator.MDExCircularProgressIndicator.render_determinate_wave**

---

## API - [`kivymd.uix.filemanager.filemanager`](https://kivymd.readthedocs.io/en/latest/components/filemanager/)

**kivymd.uix.filemanager.filemanager.MDFileManager**

Implements a modal dialog with a file manager.
For more information, see in the
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`RelativeLayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#kivy.uix.relativelayout.RelativeLayout)
classes documentation.

**kivymd.uix.filemanager.filemanager.MDFileManager.icon**

Icon that will be used on the directory selection button.
Deprecated since version 1.1.0:Use [`icon_selection_button`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.icon_selection_button) instead.
[`icon`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.icon) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to check.

**kivymd.uix.filemanager.filemanager.MDFileManager.icon_selection_button**

Icon that will be used on the directory selection button.
Added in version 1.1.0.

[`icon_selection_button`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.icon_selection_button) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to check.

**kivymd.uix.filemanager.filemanager.MDFileManager.background_color_selection_button**

Background color in (r, g, b, a) or string format of the current
directory/path selection button.
Added in version 1.1.0.

[`background_color_selection_button`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.background_color_selection_button) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.filemanager.filemanager.MDFileManager.background_color_toolbar**

Background color in (r, g, b, a) or string format of the file manager toolbar.
Added in version 1.1.0.

[`background_color_toolbar`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.background_color_toolbar) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.filemanager.filemanager.MDFileManager.icon_folder**

Icon that will be used for folder icons when using `preview = True`.

[`icon`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.icon) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to check.

**kivymd.uix.filemanager.filemanager.MDFileManager.icon_color**

Color in (r, g, b, a) or string format of the folder icon when the
[`preview`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.preview) property is set to False.
Added in version 1.1.0.

[`icon_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.icon_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.filemanager.filemanager.MDFileManager.exit_manager**

Function called when the user reaches directory tree root.
[`exit_manager`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.exit_manager) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to lambda x: None.

**kivymd.uix.filemanager.filemanager.MDFileManager.select_path**

Function, called when selecting a file/directory.
[`select_path`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.select_path) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to lambda x: None.

**kivymd.uix.filemanager.filemanager.MDFileManager.ext**

List of file extensions to be displayed in the manager.
For example, [‘.py’, ‘.kv’] - will filter out all files,
except python scripts and Kv Language.
[`ext`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.ext) is an [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [].

**kivymd.uix.filemanager.filemanager.MDFileManager.search**

It can take the values ‘all’ ‘dirs’ ‘files’ - display only directories
or only files or both them. By default, it displays folders, and files.
Available options are: ‘all’, ‘dirs’, ‘files’.
[`search`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.search) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to all.

**kivymd.uix.filemanager.filemanager.MDFileManager.current_path**

Current directory.
[`current_path`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.current_path) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to os.path.expanduser(“~”).

**kivymd.uix.filemanager.filemanager.MDFileManager.use_access**

Show access to files and directories.
[`use_access`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.use_access) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivymd.uix.filemanager.filemanager.MDFileManager.preview**

Shows only image previews.
[`preview`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.preview) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.filemanager.filemanager.MDFileManager.show_hidden_files**

Shows hidden files.
[`show_hidden_files`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.show_hidden_files) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.filemanager.filemanager.MDFileManager.sort_by**

It can take the values ‘nothing’ ‘name’ ‘date’ ‘size’ ‘type’ - sorts files
by option. By default, sort by name.
Available options are: ‘nothing’, ‘name’, ‘date’, ‘size’, ‘type’.
[`sort_by`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.sort_by) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to name.

**kivymd.uix.filemanager.filemanager.MDFileManager.sort_by_desc**

Sort by descending.
[`sort_by_desc`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.sort_by_desc) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.filemanager.filemanager.MDFileManager.selector**

It can take the values ‘any’ ‘file’ ‘folder’ ‘multi’
By default, any.
Available options are: ‘any’, ‘file’, ‘folder’, ‘multi’.
[`selector`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.selector) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to any.

**kivymd.uix.filemanager.filemanager.MDFileManager.selection**

Contains the list of files that are currently selected.
[`selection`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.selection) is a read-only [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [].

**kivymd.uix.filemanager.filemanager.MDFileManager.selection_button**

The instance of the directory/path selection button.
Added in version 1.1.0.
[`selection_button`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.selection_button) is a read-only [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivymd.uix.filemanager.filemanager.MDFileManager.show_disks**

**kivymd.uix.filemanager.filemanager.MDFileManager.show**

Forms the body of a directory tree.

**kivymd.uix.filemanager.filemanager.MDFileManager.get_access_string**

**kivymd.uix.filemanager.filemanager.MDFileManager.get_content**

Returns a list of the type [[Folder List], [file list]].

**kivymd.uix.filemanager.filemanager.MDFileManager.close**

Closes the file manager window.

**kivymd.uix.filemanager.filemanager.MDFileManager.select_dir_or_file**

Called by tap on the name of the directory or file.

**kivymd.uix.filemanager.filemanager.MDFileManager.back**

Returning to the branch down in the directory tree.

**kivymd.uix.filemanager.filemanager.MDFileManager.select_directory_on_press_button**

Called when a click on a floating button.

**kivymd.uix.filemanager.filemanager.MDFileManager.on_icon**

Called when the [`icon`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.icon) property is changed.

**kivymd.uix.filemanager.filemanager.MDFileManager.on_background_color_toolbar**

Called when the [`background_color_toolbar`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.filemanager.filemanager.MDFileManager.background_color_toolbar) property is changed.

**kivymd.uix.filemanager.filemanager.MDFileManager.on_pre_open**

Default pre-open event handler.
Added in version 1.1.0.

**kivymd.uix.filemanager.filemanager.MDFileManager.on_open**

Default open event handler.
Added in version 1.1.0.

**kivymd.uix.filemanager.filemanager.MDFileManager.on_pre_dismiss**

Default pre-dismiss event handler.
Added in version 1.1.0.

**kivymd.uix.filemanager.filemanager.MDFileManager.on_dismiss**

Default dismiss event handler.
Added in version 1.1.0.

---

## API - [`kivymd.uix.fitimage.fitimage`](https://kivymd.readthedocs.io/en/latest/components/fitimage/)

**kivymd.uix.fitimage.fitimage.FitImage**

Fit image class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`StencilBehavior`](https://kivymd.readthedocs.io/behaviors/stencil/#kivymd.uix.behaviors.stencil_behavior.StencilBehavior) and
`MaterialShape` and
[`AsyncImage`](https://kivy.org/doc/stable/api-kivy.uix.image.html#kivy.uix.image.AsyncImage) and
classes documentation.

**kivymd.uix.fitimage.fitimage.FitImage.fit_mode**

Image will be stretched horizontally or vertically to fill the widget box,
**maintaining its aspect ratio**. If the image has a different aspect ratio
than the widget, then the image will be clipped to fit.
[`fit_mode`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.fitimage.fitimage.FitImage.fit_mode) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘cover’.

**kivymd.uix.fitimage.fitimage.FitImage.shape**

The Material shape style applied to the image clipping mask.
Added in version 2.0.1.
Available shape options are: ‘circle’, ‘square’, ‘slanted’, ‘arch’,
‘semiCircle’, ‘oval’, ‘pill’, ‘triangle’, ‘arrow’, ‘fan’,
‘diamond’, ‘clamShell’, ‘pentagon’, ‘gem’, ‘sunny’,
‘verySunny’, ‘cookie4Sided’, ‘cookie6Sided’, ‘cookie7Sided’,
‘cookie9Sided’, ‘cookie12Sided’, ‘clover4Leaf’, ‘clover8Leaf’,
‘burst’, ‘softBurst’, ‘boom’, ‘softBoom’, ‘flower’, ‘puffy’,
‘puffyDiamond’, ‘ghostish’, ‘pixelCircle’, ‘pixelTriangle’,
‘bun’, ‘heart’.
If set to `None`, the image will be rendered as a standard rectangle.
[`shape`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.fitimage.fitimage.FitImage.shape) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to None.
Imperative Python StylesDeclarative Python Styles

**kivymd.uix.fitimage.fitimage.FitImage.on_source**

Fired when the `source` value changes.

**kivymd.uix.fitimage.fitimage.FitImage.update_texture**

Updates the widget texture.
If a custom Material [`shape`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.fitimage.fitimage.FitImage.shape) is set, delegates texture generation
to `materialshapes.kivy_widget.MaterialShape.update_texture()`.
This builds a Cairo surface based on the target shape dimensions,
applies the image pattern (or fill color), and renders the resulting
vector mask directly to the Kivy `texture`.
If [`shape`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.fitimage.fitimage.FitImage.shape) is `None`, execution falls back to standard GPU
texture rendering via [`AsyncImage`](https://kivy.org/doc/stable/api-kivy.uix.image.html#kivy.uix.image.AsyncImage).

---

## API - [`kivymd.uix.floatlayout`](https://kivymd.readthedocs.io/en/latest/components/floatlayout/)

**kivymd.uix.floatlayout.MDFloatLayout**

Float layout class.
For more information see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`FloatLayout`](https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html#kivy.uix.floatlayout.FloatLayout) and
[`MDAdaptiveWidget`](https://kivymd.readthedocs.io/api/kivymd/uix/#kivymd.uix.MDAdaptiveWidget)
classes documentation.

---

## API - [`kivymd.uix.gridlayout`](https://kivymd.readthedocs.io/en/latest/components/gridlayout/)

**kivymd.uix.gridlayout.MDGridLayout**

Grid layout class.
For more information see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`GridLayout`](https://kivy.org/doc/stable/api-kivy.uix.gridlayout.html#kivy.uix.gridlayout.GridLayout) and
[`MDAdaptiveWidget`](https://kivymd.readthedocs.io/api/kivymd/uix/#kivymd.uix.MDAdaptiveWidget)
classes documentation.

---

## API - [`kivymd.uix.hero`](https://kivymd.readthedocs.io/en/latest/components/hero/)

**kivymd.uix.hero.MDHeroFrom**

The container from which the hero begins his flight.
For more information, see in the
[`MDBoxLayout`](https://kivymd.readthedocs.io/en/boxlayout/#kivymd.uix.boxlayout.MDBoxLayout) class documentation.

**kivymd.uix.hero.MDHeroFrom.tag**

Tag ID for heroes.
[`tag`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.hero.MDHeroFrom.tag) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘’.

**kivymd.uix.hero.MDHeroFrom.on_transform_in**

Fired when the hero flies from screen **A** to screen **B**.

**kivymd.uix.hero.MDHeroFrom.on_transform_out**

Fired when the hero back from screen **B** to screen **A**.

**kivymd.uix.hero.MDHeroTo**

The container in which the hero comes.
For more information, see in the
[`MDBoxLayout`](https://kivymd.readthedocs.io/en/boxlayout/#kivymd.uix.boxlayout.MDBoxLayout) class documentation.

**kivymd.uix.hero.MDHeroTo.tag**

Tag ID for heroes.
[`tag`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.hero.MDHeroTo.tag) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘’.

---

## API - [`kivymd.uix.imagelist.imagelist`](https://kivymd.readthedocs.io/en/latest/components/imagelist/)

**kivymd.uix.imagelist.imagelist.MDSmartTileImage**

Implements the tile image.
Changed in version 2.0.0:The SmartTileImage class has been renamed to MDSmartTileImage.
For more information, see in the
[`RectangularRippleBehavior`](https://kivymd.readthedocs.io/behaviors/ripple/#id0) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
[`FitImage`](https://kivymd.readthedocs.io/en/fitimage/#kivymd.uix.fitimage.fitimage.FitImage)
classes documentation.

**kivymd.uix.imagelist.imagelist.MDSmartTileImage.on_touch_down**

Receive a touch down event.

**kivymd.uix.imagelist.imagelist.MDSmartTileOverlayContainer**

Implements a container for custom widgets to be added to the tile.
Changed in version 2.0.0:The SmartTileOverlayBox class has been renamed to
MDSmartTileOverlayContainer.
For more information, see in the
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout) class documentation.

**kivymd.uix.imagelist.imagelist.MDSmartTileOverlayContainer.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.imagelist.imagelist.MDSmartTile**

A tile for more complex needs.
For more information, see in the
[`MDRelativeLayout`](https://kivymd.readthedocs.io/en/relativelayout/#kivymd.uix.relativelayout.MDRelativeLayout)
class documentation.
Includes an image, a container to place overlays and a box that can act
as a header or a footer, as described in the Material Design specs.

**kivymd.uix.imagelist.imagelist.MDSmartTile.overlay_mode**

Determines weather the information box acts as a header or footer to the
image. Available are options: ‘footer’, ‘header’.
Changed in version 2.0.0:The box_position attribute has been renamed to overlay_mode.

[`overlay_mode`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.imagelist.imagelist.MDSmartTile.overlay_mode) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘footer’.

**kivymd.uix.imagelist.imagelist.MDSmartTile.overlap**

Determines if the header/footer overlaps on top of the image or not.

[`overlap`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.imagelist.imagelist.MDSmartTile.overlap) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivymd.uix.imagelist.imagelist.MDSmartTile.ripple_effect**

**kivymd.uix.imagelist.imagelist.MDSmartTile.on_release**

Fired when the button is released (i.e. the touch/click that
pressed the button goes away).

**kivymd.uix.imagelist.imagelist.MDSmartTile.on_press**

Fired when the button is pressed.

**kivymd.uix.imagelist.imagelist.MDSmartTile.add_widget**

Add a new widget as a child of this widget.

---

## API - [`kivymd.uix.label.label`](https://kivymd.readthedocs.io/en/latest/components/label/)

**kivymd.uix.label.label.MDLabel**

Label class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`Label`](https://kivy.org/doc/stable/api-kivy.uix.label.html#kivy.uix.label.Label) and
[`MDAdaptiveWidget`](https://kivymd.readthedocs.io/api/kivymd/uix/#kivymd.uix.MDAdaptiveWidget) and
[`TouchBehavior`](https://kivymd.readthedocs.io/behaviors/touch/#kivymd.uix.behaviors.touch_behavior.TouchBehavior) and
[`StateLayerBehavior`](https://kivymd.readthedocs.io/behaviors/state-layer/#kivymd.uix.behaviors.state_layer_behavior.StateLayerBehavior)
classes documentation.

**kivymd.uix.label.label.MDLabel.font_style**

Label font style.
Changed in version 2.0.0.
Available vanilla font_style are: ‘Display’, ‘Headline’, ‘Title’,
‘Label’, ‘Body’`.
[`font_style`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel.font_style) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘Body’.

**kivymd.uix.label.label.MDLabel.role**

Role of font style.
Added in version 2.0.0.
Available options are: ‘large’, ‘medium’, ‘small’.
[`role`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel.role) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘large’.

**kivymd.uix.label.label.MDLabel.text**

Text of the label.
[`text`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel.text) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘’.

**kivymd.uix.label.label.MDLabel.text_color**

Label text color in (r, g, b, a) or string format.
[`text_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel.text_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.label.label.MDLabel.text_color_disabled**

Label text color in (r, g, b, a) or string format.
Added in version 2.0.1.
[`text_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel.text_color_disabled) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.label.label.MDLabel.allow_copy**

Allows you to copy text to the clipboard by double-clicking on the label.
Added in version 1.2.0.
[`allow_copy`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel.allow_copy) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.label.label.MDLabel.allow_selection**

Allows to highlight text by double-clicking on the label.
Added in version 1.2.0.
[`allow_selection`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel.allow_selection) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.label.label.MDLabel.color_selection**

The color in (r, g, b, a) or string format of the text selection when the
value of the [`allow_selection`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel.allow_selection) attribute is True.
Added in version 1.2.0.
[`color_selection`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel.color_selection) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.label.label.MDLabel.color_deselection**

The color in (r, g, b, a) or string format of the text deselection when the
value of the [`allow_selection`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel.allow_selection) attribute is True.
Added in version 1.2.0.
[`color_deselection`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel.color_deselection) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.label.label.MDLabel.is_selected**

Is the label text highlighted.
Added in version 1.2.0.
[`is_selected`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel.is_selected) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.label.label.MDLabel.radius**

Label radius.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel.radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [0, 0, 0, 0].

**kivymd.uix.label.label.MDLabel.do_selection**

**kivymd.uix.label.label.MDLabel.cancel_selection**

**kivymd.uix.label.label.MDLabel.on_double_tap**

Fired by double-clicking on the widget.

**kivymd.uix.label.label.MDLabel.on_window_touch**

Fired at the on_touch_down event.

**kivymd.uix.label.label.MDLabel.on_copy**

Fired when double-tapping on the label.
Added in version 1.2.0.

**kivymd.uix.label.label.MDLabel.on_selection**

Fired when double-tapping on the label.
Added in version 1.2.0.

**kivymd.uix.label.label.MDLabel.on_cancel_selection**

Fired when the highlighting is removed from the label text.
Added in version 1.2.0.

**kivymd.uix.label.label.MDLabel.on_allow_selection**

Fired when the [`allow_selection`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel.allow_selection) value changes.

**kivymd.uix.label.label.MDLabel.on_text_color**

Fired when the [`text_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel.text_color) value changes.

**kivymd.uix.label.label.MDLabel.on_md_bg_color**

Fired when the `md_bg_color` value changes.

**kivymd.uix.label.label.MDLabel.on_size**

Fired when the parent window of the application is resized.

**kivymd.uix.label.label.MDLabel.update_canvas_bg_pos**

**kivymd.uix.label.label.MDIcon**

Icon class.
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDLabel) class documentation.

**kivymd.uix.label.label.MDIcon.icon**

Label icon name.
[`icon`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDIcon.icon) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘blank’.

**kivymd.uix.label.label.MDIcon.source**

Path to icon.
[`source`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDIcon.source) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to None.

**kivymd.uix.label.label.MDIcon.icon_color**

Icon color in (r, g, b, a) or string format.
Added in version 2.0.0.
[`icon_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDIcon.icon_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.label.label.MDIcon.icon_color_disabled**

The icon color in (r, g, b, a) or string format of the button when
the button is disabled.
Added in version 2.0.0.
[`icon_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.label.label.MDIcon.icon_color_disabled) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.label.label.MDIcon.add_widget**

Add a new widget as a child of this widget.

---

## API - [`kivymd.uix.list.list`](https://kivymd.readthedocs.io/en/latest/components/list/)

**kivymd.uix.list.list.MDList**

ListItem container.
Best used in conjunction with a `kivy.uix.ScrollView`.
When adding (or removing) a widget, it will resize itself to fit its
children, plus top and bottom paddings as described by the MD spec.
For more information, see in the
[`MDGridLayout`](https://kivymd.readthedocs.io/en/gridlayout/#kivymd.uix.gridlayout.MDGridLayout) class documentation.

**kivymd.uix.list.list.BaseListItem**

Base class for list items.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`RectangularRippleBehavior`](https://kivymd.readthedocs.io/behaviors/ripple/#id0) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
`StateLayerBehavior`
classes documentation.

**kivymd.uix.list.list.BaseListItem.divider**

Should I use divider for a list item.
[`divider`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.list.list.BaseListItem.divider) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.list.list.BaseListItem.divider_color**

The divider color in (r, g, b, a) or string format.
[`divider_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.list.list.BaseListItem.divider_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.list.list.BaseListItem.md_bg_color_disabled**

The background color in (r, g, b, a) or string format of the list item when
the list item is disabled.
[`md_bg_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.list.list.BaseListItem.md_bg_color_disabled) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.list.list.BaseListItemText**

Base class for text labels of a list item.
For more information, see in the [`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel)
class documentation.

**kivymd.uix.list.list.BaseListItemIcon**

Base class for leading/trailing icon of list item.
For more information, see in the [`MDIcon`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDIcon)
class documentation.

**kivymd.uix.list.list.BaseListItemIcon.icon_color**

Icon color in (r, g, b, a) or string format.
[`icon_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.list.list.BaseListItemIcon.icon_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.list.list.BaseListItemIcon.icon_color_disabled**

The icon color in (r, g, b, a) or string format of the list item when
the list item is disabled.
[`icon_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.list.list.BaseListItemIcon.icon_color_disabled) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.list.list.MDListItemHeadlineText**

Implements a class for headline text of list item.
For more information, see in the [`BaseListItemText`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.list.list.BaseListItemText)
class documentation.

**kivymd.uix.list.list.MDListItemSupportingText**

Implements a class for secondary text of list item.
For more information, see in the [`BaseListItemText`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.list.list.BaseListItemText)
class documentation.

**kivymd.uix.list.list.MDListItemTertiaryText**

Implements a class for tertiary text of list item.
For more information, see in the [`BaseListItemText`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.list.list.BaseListItemText)
class documentation.

**kivymd.uix.list.list.MDListItemTrailingSupportingText**

Implements a class for trailing text of list item.
For more information, see in the [`BaseListItemText`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.list.list.BaseListItemText)
class documentation.

**kivymd.uix.list.list.MDListItemLeadingIcon**

Implements a class for leading icon class.
For more information, see in the [`BaseListItemIcon`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.list.list.BaseListItemIcon)
class documentation.

**kivymd.uix.list.list.MDListItemLeadingAvatar**

Implements a class for leading avatar class.
For more information, see in the
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`CircularRippleBehavior`](https://kivymd.readthedocs.io/behaviors/ripple/#id1) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
[`FitImage`](https://kivymd.readthedocs.io/en/fitimage/#kivymd.uix.fitimage.fitimage.FitImage)
classes documentation.

**kivymd.uix.list.list.MDListItemTrailingIcon**

Implements a class for trailing icon class.
For more information, see in the [`BaseListItemIcon`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.list.list.BaseListItemIcon)
class documentation.

**kivymd.uix.list.list.MDListItemTrailingCheckbox**

Implements a class for trailing checkbox class.
For more information, see in the
[`MDCheckbox`](https://kivymd.readthedocs.io/en/selectioncontrols/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox)
class documentation.

**kivymd.uix.list.list.MDListItem**

Implements a list item.
For more information, see in the
[`BaseListItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.list.list.BaseListItem) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
classes documentation.

**kivymd.uix.list.list.MDListItem.add_widget**

Add a new widget as a child of this widget.

---

## API - [`kivymd.uix.loadingindicator.loadingindicator`](https://kivymd.readthedocs.io/en/latest/components/loadingindicator/)

**kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator**

Implementation of a morphing and rotating loading indicator.
For more information, see the
[`AnchorLayout`](https://kivy.org/doc/stable/api-kivy.uix.anchorlayout.html#kivy.uix.anchorlayout.AnchorLayout) and
`RotateBehavior`
classes documentation.

**kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.shape**

Current shape name displayed by the loading indicator.
The shape corresponds to one of the predefined shapes available
in the `MaterialShape` library.
You can view all available shape names using
[`get_shape_names()`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.get_shape_names).
[`shape`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.shape) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘cookie12Sided’.

**kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.shape_sequence**

Sequence of shape names through which the indicator cycles.
Each shape in the list is morphed into the next one over time,
looping continuously while the indicator is active.
[`shape_sequence`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.shape_sequence) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to:

**kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.shape_size**

Size of the loading indicator.
[`shape_size`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.shape_size) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to dp(48).

**kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.duration**

Duration of one morph-and-rotate cycle in seconds.
This value controls the overall speed of the loading indicator.
[`duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.65.

**kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.active_indicator_color**

Color of the active (foreground) loading shape.
[`active_indicator_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.active_indicator_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to [0, 0, 0, 0].

**kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.container_color**

Background container color of the indicator.
[`container_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.container_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to [0, 0, 0, 0].

**kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.shape_index**

Current index in the [`shape_sequence`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.shape_sequence).
[`shape_index`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.shape_index) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.start**

Start the loading animation.
Initiates the shape morphing and rotation cycle.
The indicator continuously transitions between the shapes defined in
[`shape_sequence`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.shape_sequence) while rotating at regular intervals.
If already active, the animation sequence is reset.

**kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.stop**

Stop the loading animation.

**kivymd.uix.loadingindicator.loadingindicator.MDLoadingIndicator.get_shape_names**

Return all available material shape names.

---

## API - [`kivymd.uix.menu.menu`](https://kivymd.readthedocs.io/en/latest/components/menu/)

**kivymd.uix.menu.menu.BaseDropdownItem**

Base class for menu items.
Added in version 1.2.0.
For more information, see in the
[`RectangularRippleBehavior`](https://kivymd.readthedocs.io/behaviors/ripple/#id0) and
[`MDBoxLayout`](https://kivymd.readthedocs.io/en/boxlayout/#kivymd.uix.boxlayout.MDBoxLayout) classes.

**kivymd.uix.menu.menu.BaseDropdownItem.text**

The text of the menu item.
[`text`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem.text) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘’.

**kivymd.uix.menu.menu.BaseDropdownItem.leading_icon**

The leading icon of the menu item.
[`leading_icon`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem.leading_icon) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘’.

**kivymd.uix.menu.menu.BaseDropdownItem.trailing_icon**

The trailing icon of the menu item.
[`trailing_icon`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem.trailing_icon) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘’.

**kivymd.uix.menu.menu.BaseDropdownItem.trailing_text**

The trailing text of the menu item.
[`trailing_text`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem.trailing_text) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘’.

**kivymd.uix.menu.menu.BaseDropdownItem.text_color**

The color of the text in (r, g, b, a) or string format for the text of the
menu item.
[`text_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem.text_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.menu.menu.BaseDropdownItem.leading_icon_color**

The color of the text in (r, g, b, a) or string format for the leading icon
of the menu item.
[`leading_icon_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem.leading_icon_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.menu.menu.BaseDropdownItem.trailing_icon_color**

The color of the text in (r, g, b, a) or string format for the trailing
icon of the menu item.
[`leading_icon_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem.leading_icon_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.menu.menu.BaseDropdownItem.trailing_text_color**

The color of the text in (r, g, b, a) or string format for the trailing
text of the menu item.
[`leading_icon_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem.leading_icon_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.menu.menu.BaseDropdownItem.divider**

Divider mode. Available options are: ‘Full’, None
and default to ‘Full’.
[`divider`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem.divider) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘Full’.

**kivymd.uix.menu.menu.BaseDropdownItem.divider_color**

Divider color in (r, g, b, a) or string format.
[`divider_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem.divider_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.menu.menu.MDDropdownTextItem**

Implements a menu item with text without leading and trailing icons.
Added in version 1.2.0.
For more information, see in the [`BaseDropdownItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem) class.

**kivymd.uix.menu.menu.MDDropdownLeadingIconItem**

Implements a menu item with text, leading icon and without trailing icon.
Added in version 1.2.0.
For more information, see in the [`BaseDropdownItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem) class.

**kivymd.uix.menu.menu.MDDropdownTrailingIconItem**

Implements a menu item with text, without leading icon and with trailing
icon.
Added in version 1.2.0.
For more information, see in the [`BaseDropdownItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem) class.

**kivymd.uix.menu.menu.MDDropdownTrailingIconTextItem**

Implements a menu item with text, without leading icon, with trailing
icon and with trailing text.
Added in version 1.2.0.
For more information, see in the [`BaseDropdownItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem) class.

**kivymd.uix.menu.menu.MDDropdownTrailingTextItem**

Implements a menu item with text, without leading icon, without trailing
icon and with trailing text.
Added in version 1.2.0.
For more information, see in the [`BaseDropdownItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem) class.

**kivymd.uix.menu.menu.MDDropdownLeadingIconTrailingTextItem**

Implements a menu item with text, leading icon and with trailing text.
Added in version 1.2.0.
For more information, see in the [`BaseDropdownItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem) class.

**kivymd.uix.menu.menu.MDDropdownLeadingTrailingIconTextItem**

Implements a menu item with text, with leading icon, with trailing
icon and with trailing text.
Added in version 1.2.0.
For more information, see in the [`BaseDropdownItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.BaseDropdownItem) class.

**kivymd.uix.menu.menu.MDDropdownMenu**

Dropdown menu class.
For more information, see in the
[`MotionDropDownMenuBehavior`](https://kivymd.readthedocs.io/behaviors/motion/#kivymd.uix.behaviors.motion_behavior.MotionDropDownMenuBehavior) and
[`StencilBehavior`](https://kivymd.readthedocs.io/behaviors/stencil/#kivymd.uix.behaviors.stencil_behavior.StencilBehavior) and
[`MDCard`](https://kivymd.readthedocs.io/en/card/#kivymd.uix.card.card.MDCard)
classes documentation.

**kivymd.uix.menu.menu.MDDropdownMenu.header_cls**

An instance of the class (Kivy or KivyMD widget) that will be added
to the menu header.
Added in version 0.104.2.
See [Header](https://kivymd.readthedocs.io/en/latest/#header) for more information.
[`header_cls`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.MDDropdownMenu.header_cls) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivymd.uix.menu.menu.MDDropdownMenu.items**

List of dictionaries with properties for menu items.
[`items`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.MDDropdownMenu.items) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [].

**kivymd.uix.menu.menu.MDDropdownMenu.width_mult**

This number multiplied by the standard increment (‘56dp’ on mobile, ‘64dp’
on desktop), determines the width of the menu items.
If the resulting number were to be too big for the application Window,
the multiplier will be adjusted for the biggest possible one.
Deprecated since version 1.2.0:Use width instead.
[`width_mult`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.MDDropdownMenu.width_mult) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 1.

**kivymd.uix.menu.menu.MDDropdownMenu.min_height**

**kivymd.uix.menu.menu.MDDropdownMenu.max_height**

The menu will grow no bigger than this number. Set to 0 for no limit.
[`max_height`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.MDDropdownMenu.max_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivymd.uix.menu.menu.MDDropdownMenu.border_margin**

Margin between Window border and menu.

[`border_margin`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.MDDropdownMenu.border_margin) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 4dp.

**kivymd.uix.menu.menu.MDDropdownMenu.ver_growth**

Where the menu will grow vertically to when opening. Set to None to let
the widget pick for you. Available options are: ‘up’, ‘down’.

[`ver_growth`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.MDDropdownMenu.ver_growth) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to None.

**kivymd.uix.menu.menu.MDDropdownMenu.hor_growth**

Where the menu will grow horizontally to when opening. Set to None to let
the widget pick for you. Available options are: ‘left’, ‘right’.

[`hor_growth`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.MDDropdownMenu.hor_growth) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to None.

**kivymd.uix.menu.menu.MDDropdownMenu.background_color**

Color in (r, g, b, a) or string format of the background of the menu.
Deprecated since version 1.2.0:Use md_bg_color instead.
[`background_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.MDDropdownMenu.background_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.menu.menu.MDDropdownMenu.caller**

The widget object that calls the menu window.
[`caller`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.MDDropdownMenu.caller) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivymd.uix.menu.menu.MDDropdownMenu.position**

Menu window position relative to parent element.
Available options are: ‘auto’, ‘top’, ‘center’, ‘bottom’.
See [Position](https://kivymd.readthedocs.io/en/latest/#position) for more information.
[`position`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.MDDropdownMenu.position) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘auto’.

**kivymd.uix.menu.menu.MDDropdownMenu.radius**

Menu radius.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.MDDropdownMenu.radius) is a [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to ‘[dp(7)]’.

**kivymd.uix.menu.menu.MDDropdownMenu.scrim_color**

Color for scrim in (r, g, b, a) or string format.
[`scrim_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.MDDropdownMenu.scrim_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to [0, 0, 0, 0.5].

**kivymd.uix.menu.menu.MDDropdownMenu.adjust_width**

Adjust the width of the menu if the width of the menu goes beyond
the boundaries of the parent window from starting point.

**kivymd.uix.menu.menu.MDDropdownMenu.check_ver_growth**

Checks whether the height of the lower/upper borders of the menu
exceeds the limits borders of the parent window.

**kivymd.uix.menu.menu.MDDropdownMenu.check_hor_growth**

Checks whether the width of the left/right menu borders exceeds the
boundaries of the parent window.

**kivymd.uix.menu.menu.MDDropdownMenu.get_target_pos**

**kivymd.uix.menu.menu.MDDropdownMenu.set_target_height**

Set the target height of the menu depending on the size of each item.

**kivymd.uix.menu.menu.MDDropdownMenu.set_menu_properties**

Sets the size and position for the menu window.

**kivymd.uix.menu.menu.MDDropdownMenu.set_menu_pos**

**kivymd.uix.menu.menu.MDDropdownMenu.adjust_position**

Return value ‘auto’ for the menu position if the menu position is out
of screen.

**kivymd.uix.menu.menu.MDDropdownMenu.open**

Animate the opening of a menu window.

**kivymd.uix.menu.menu.MDDropdownMenu.on_items**

The method sets the class that will be used to create the menu item.

**kivymd.uix.menu.menu.MDDropdownMenu.on_header_cls**

Called when a value is set to the [`header_cls`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.MDDropdownMenu.header_cls) parameter.

**kivymd.uix.menu.menu.MDDropdownMenu.on_touch_down**

Receive a touch down event.

**kivymd.uix.menu.menu.MDDropdownMenu.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.MDDropdownMenu.on_touch_down) for more information.

**kivymd.uix.menu.menu.MDDropdownMenu.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.menu.menu.MDDropdownMenu.on_touch_down) for more information.

**kivymd.uix.menu.menu.MDDropdownMenu.dismiss**

Closes the menu.

---

## API - [`kivymd.uix.navigationbar.navigationbar`](https://kivymd.readthedocs.io/en/latest/components/navigation-bar/)

**kivymd.uix.navigationbar.navigationbar.MDNavigationItemLabel**

Implements a text label for the [`MDNavigationItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationbar.navigationbar.MDNavigationItem) class.
Added in version 2.0.0.
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) class documentation.

**kivymd.uix.navigationbar.navigationbar.MDNavigationItemLabel.text_color_active**

Item icon color in (r, g, b, a) or string format.
[`text_color_active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationbar.navigationbar.MDNavigationItemLabel.text_color_active) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.navigationbar.navigationbar.MDNavigationItemLabel.text_color_normal**

Item icon color in (r, g, b, a) or string format.
[`text_color_normal`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationbar.navigationbar.MDNavigationItemLabel.text_color_normal) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.navigationbar.navigationbar.MDNavigationItemIcon**

Implements a icon for the [`MDNavigationItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationbar.navigationbar.MDNavigationItem) class.
Added in version 2.0.0.
For more information, see in the
[`MDIcon`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDIcon) class documentation.

**kivymd.uix.navigationbar.navigationbar.MDNavigationItemIcon.icon_color_active**

Item icon color in (r, g, b, a) or string format.
[`icon_color_active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationbar.navigationbar.MDNavigationItemIcon.icon_color_active) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.navigationbar.navigationbar.MDNavigationItemIcon.icon_color_normal**

Item icon color in (r, g, b, a) or string format.
[`icon_color_normal`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationbar.navigationbar.MDNavigationItemIcon.icon_color_normal) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.navigationbar.navigationbar.MDNavigationItem**

Bottom item class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`RectangularRippleBehavior`](https://kivymd.readthedocs.io/behaviors/ripple/#id0) and
[`AnchorLayout`](https://kivy.org/doc/stable/api-kivy.uix.anchorlayout.html#kivy.uix.anchorlayout.AnchorLayout) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior)
classes documentation.
Changed in version 2.0.0:Rename class from MDBottomNavigationItem to MDNavigationItem.

**kivymd.uix.navigationbar.navigationbar.MDNavigationItem.active**

Indicates if the bar item is active or inactive.
[`active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationbar.navigationbar.MDNavigationItem.active) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.navigationbar.navigationbar.MDNavigationItem.indicator_color**

The background color in (r, g, b, a) or string format of the highlighted
item.
Added in version 1.0.0.
Changed in version 2.0.0:Rename property from selected_color_background to indicator_color.
[`indicator_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationbar.navigationbar.MDNavigationItem.indicator_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.navigationbar.navigationbar.MDNavigationItem.indicator_transition**

Animation type of the active element indicator.
[`indicator_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationbar.navigationbar.MDNavigationItem.indicator_transition) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘in_out_sine’.

**kivymd.uix.navigationbar.navigationbar.MDNavigationItem.indicator_duration**

Duration of animation of the active element indicator.
[`indicator_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationbar.navigationbar.MDNavigationItem.indicator_duration) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.1.

**kivymd.uix.navigationbar.navigationbar.MDNavigationItem.on_active**

Fired when the values of [`active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationbar.navigationbar.MDNavigationItem.active) change.

**kivymd.uix.navigationbar.navigationbar.MDNavigationItem.on_release**

Fired when clicking on a panel item.

**kivymd.uix.navigationbar.navigationbar.MDNavigationItem.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.navigationbar.navigationbar.MDNavigationBar**

A navigation bar class.
For more information, see in the
[`CommonElevationBehavior`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior) and
[`MDBoxLayout`](https://kivymd.readthedocs.io/en/boxlayout/#kivymd.uix.boxlayout.MDBoxLayout)
classes documentation.

Changed in version 2.0.0:Rename class from MDBottomNavigation to MDNavigationBar.

**kivymd.uix.navigationbar.navigationbar.MDNavigationBar.set_bars_color**

If True the background color of the navigation bar will be set
automatically according to the current color of the toolbar.
Added in version 1.0.0.
[`set_bars_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationbar.navigationbar.MDNavigationBar.set_bars_color) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.navigationbar.navigationbar.MDNavigationBar.get_active_item**

Returns the currently active item in the navigation bar.
Added in version 2.0.0.

**kivymd.uix.navigationbar.navigationbar.MDNavigationBar.set_active_item**

Sets the currently active element on the panel.

**kivymd.uix.navigationbar.navigationbar.MDNavigationBar.set_status_bar_color**

Sets the color of the lower system navigation bar.

**kivymd.uix.navigationbar.navigationbar.MDNavigationBar.on_switch_tabs**

Fired when switching tabs.

---

## API - [`kivymd.uix.navigationdrawer.navigationdrawer`](https://kivymd.readthedocs.io/en/latest/components/navigationdrawer/)

**kivymd.uix.navigationdrawer.navigationdrawer.BaseNavigationDrawerItem**

Implement the base class for the menu list item.
Added in version 2.0.0.

**kivymd.uix.navigationdrawer.navigationdrawer.BaseNavigationDrawerItem.selected**

Is the item selected.
[`selected`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.BaseNavigationDrawerItem.selected) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationLayout**

For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`FloatLayout`](https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html#kivy.uix.floatlayout.FloatLayout)
classes documentation.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationLayout.update_pos**

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationLayout.add_scrim**

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationLayout.update_scrim_rectangle**

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationLayout.add_widget**

Only two layouts are allowed:
[`ScreenManager`](https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html#kivy.uix.screenmanager.ScreenManager) and
[`MDNavigationDrawer`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer).

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerLabel**

Implements a label class.
For more information, see in the [`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel)
class documentation.
Added in version 1.0.0.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerDivider**

Implements a divider class.
For more information, see in the
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout) class documentation.
Added in version 1.0.0.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerHeader**

Implements a header class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
classes documentation.
Added in version 1.0.0.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerItem**

Implements an item for the [`MDNavigationDrawer`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer) menu list.
For more information, see in the
[`MDListItem`](https://kivymd.readthedocs.io/en/list/#kivymd.uix.list.list.MDListItem) and
[`StateFocusBehavior`](https://kivymd.readthedocs.io/behaviors/focus/#kivymd.uix.behaviors.focus_behavior.StateFocusBehavior) and
[`BaseNavigationDrawerItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.BaseNavigationDrawerItem)
classes documentation.
Added in version 1.0.0.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerItem.active_indicator_color**

The active indicator color in (r, g, b, a) or string format.
Added in version 2.0.0.
[`active_indicator_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerItem.active_indicator_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerItem.inactive_indicator_color**

The inactive indicator color in (r, g, b, a) or string format.
Added in version 2.0.0.
[`inactive_indicator_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerItem.inactive_indicator_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerItem.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerItem.on_release**

Fired when the item is released
(i.e. the touch/click that pressed the item goes away).

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerItem.on_selected**

Fired when the `selected` value changes

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerItemLeadingIcon**

Implements the leading icon for the menu list item.
For more information, see in the
[`MDListItemLeadingIcon`](https://kivymd.readthedocs.io/en/list/#kivymd.uix.list.list.MDListItemLeadingIcon) and
[`BaseNavigationDrawerItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.BaseNavigationDrawerItem)
classes documentation.
Added in version 2.0.0.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerItemText**

Implements the text for the menu list item.
For more information, see in the
[`MDListItemSupportingText`](https://kivymd.readthedocs.io/en/list/#kivymd.uix.list.list.MDListItemSupportingText) and
[`BaseNavigationDrawerItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.BaseNavigationDrawerItem)
classes documentation.
Added in version 2.0.0.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerItemTrailingText**

Implements the supporting text for the menu list item.
For more information, see in the
[`MDListItemTrailingSupportingText`](https://kivymd.readthedocs.io/en/list/#kivymd.uix.list.list.MDListItemTrailingSupportingText) and
[`BaseNavigationDrawerItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.BaseNavigationDrawerItem)
classes documentation.
Added in version 2.0.0.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerMenu**

Implements a scrollable list for menu items of the
[`MDNavigationDrawer`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer) class.
For more information, see in the
[`MDScrollView`](https://kivymd.readthedocs.io/en/scrollview/#kivymd.uix.scrollview.MDScrollView) class documentation.
Added in version 1.0.0.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerMenu.spacing**

Spacing between children, in pixels.
[`spacing`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerMenu.spacing) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerMenu.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawerMenu.update_items_color**

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer**

Navigation drawer class.
For more information, see in the [`MDCard`](https://kivymd.readthedocs.io/en/card/#kivymd.uix.card.card.MDCard)
class documentation.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.drawer_type**

Type of drawer. Modal type will be on top of screen. Standard type will be
at left or right of screen. Also it automatically disables
[`close_on_click`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.close_on_click) and [`enable_swiping`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.enable_swiping) to prevent closing
drawer for standard type.
Changed in version 2.0.0:Rename from type to drawer_type.
[`drawer_type`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.drawer_type) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘modal’.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.anchor**

Anchoring screen edge for drawer. Set it to ‘right’ for right-to-left
languages. Available options are: ‘left’, ‘right’.
[`anchor`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.anchor) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘left’.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.scrim_color**

Color for scrim in (r, g, b, a) or string format. Alpha channel will be
multiplied with `_scrim_alpha`. Set fourth channel to 0 if you want
to disable scrim.
[`scrim_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.scrim_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to [0, 0, 0, 0.5].

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.padding**

Padding between layout box and children: [padding_left, padding_top,
padding_right, padding_bottom].
Padding also accepts a two argument form [padding_horizontal,
padding_vertical] and a one argument form [padding].
Changed in version 1.0.0.

[`padding`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.padding) is a [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty) and
defaults to ‘[dp(16), dp(16), dp(12), dp(16)]’.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.close_on_click**

Close when click on scrim or keyboard escape. It automatically sets to
False for “standard” type.
[`close_on_click`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.close_on_click) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.state**

Indicates if panel closed or opened. Sets after [`status`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.status) change.
Available options are: ‘close’, ‘open’.
[`state`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.state) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘close’.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.status**

Detailed state. Sets before [`state`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.state). Bind to [`state`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.state) instead
of [`status`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.status). Available options are: ‘closed’,
‘opening_with_swipe’, ‘opening_with_animation’, ‘opened’,
‘closing_with_swipe’, ‘closing_with_animation’.
[`status`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.status) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘closed’.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.open_progress**

Percent of visible part of side panel. The percent is specified as a
floating point number in the range 0-1. 0.0 if panel is closed and 1.0 if
panel is opened.
[`open_progress`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.open_progress) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.0.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.enable_swiping**

Allow to open or close navigation drawer with swipe. It automatically
sets to False for “standard” type.
[`enable_swiping`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.enable_swiping) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.swipe_distance**

The distance of the swipe with which the movement of navigation drawer
begins.
[`swipe_distance`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.swipe_distance) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 10.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.swipe_edge_width**

The size of the area in px inside which should start swipe to drag
navigation drawer.
[`swipe_edge_width`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.swipe_edge_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 20.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.scrim_alpha_transition**

The name of the animation transition type to use for changing
`scrim_alpha`.
[`scrim_alpha_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.scrim_alpha_transition) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘linear’.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.opening_transition**

The name of the animation transition type to use when animating to
the [`state`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.state) ‘open’.
[`opening_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.opening_transition) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘out_cubic’.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.opening_time**

The time taken for the panel to slide to the [`state`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.state) ‘open’.
[`opening_time`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.opening_time) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.closing_transition**

The name of the animation transition type to use when animating to
the [`state`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.state) ‘close’.
[`closing_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.closing_transition) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘out_sine’.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.closing_time**

The time taken for the panel to slide to the [`state`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.state) ‘close’.
[`closing_time`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.closing_time) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.background_color**

The drawer background color in (r, g, b, a) or string format.
Added in version 2.0.0.
[`background_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.background_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.theme_elevation_level**

Drawer elevation level scheme name.
Added in version 2.0.0.
Available options are: ‘Primary’, ‘Custom’.
[`theme_elevation_level`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.theme_elevation_level) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘Custom’.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.elevation_level**

Drawer elevation level (values from 0 to 5)
Added in version 2.2.0.
[`elevation_level`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.elevation_level) is an [`BoundedNumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BoundedNumericProperty)
and defaults to 2.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.set_properties_widget**

Fired on_release/on_press/on_enter/on_leave events.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.set_state**

Change state of the side panel.
New_state can be one of “toggle”, “open” or “close”.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.update_status**

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.get_dist_from_side**

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.on_touch_down**

Receive a touch down event.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.on_touch_down) for more information.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.on_touch_down) for more information.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.on_radius**

Fired when the `radius` value changes.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.on_drawer_type**

Fired when the [`drawer_type`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.drawer_type) value changes.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.on_open**

Fired when the navigation drawer is opened.

**kivymd.uix.navigationdrawer.navigationdrawer.MDNavigationDrawer.on_close**

Fired when the navigation drawer is closed.

---

## API - [`kivymd.uix.navigationrail.navigationrail`](https://kivymd.readthedocs.io/en/latest/components/navigationrail/)

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailFabButton**

Implements a floating action button (FAB).
For more information, see in the
[`MDFabButton`](https://kivymd.readthedocs.io/en/button/#kivymd.uix.button.button.MDFabButton)
class documentation.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailFabButton.md_bg_color_disabled**

The background color in (r, g, b, a) or string format of the switch when
the widget is disabled.
[`md_bg_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationrail.navigationrail.MDNavigationRailFabButton.md_bg_color_disabled) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailMenuButton**

Implements a menu button.
For more information, see in the
[`MDIconButton`](https://kivymd.readthedocs.io/en/button/#kivymd.uix.button.button.MDIconButton) class documentation.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailMenuButton.md_bg_color_disabled**

The background color in (r, g, b, a) or string format of the switch when
the widget is disabled.
[`md_bg_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationrail.navigationrail.MDNavigationRailMenuButton.md_bg_color_disabled) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailItemIcon**

Implements an icon for the [`MDNavigationRailItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationrail.navigationrail.MDNavigationRailItem) class.
For more information, see in the [`MDIcon`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDIcon)
class documentation.
Changed in version 2.0.0.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailItemIcon.active_indicator_color**

Background color of the active indicator in (r, g, b, a) or string format.
[`active_indicator_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationrail.navigationrail.MDNavigationRailItemIcon.active_indicator_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailItemLabel**

Implements an label for the [`MDNavigationRailItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationrail.navigationrail.MDNavigationRailItem) class.
For more information, see in the
[`ScaleBehavior`](https://kivymd.readthedocs.io/behaviors/scale/#kivymd.uix.behaviors.scale_behavior.ScaleBehavior) and
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel)
classes documentation.
Changed in version 2.0.0.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailItemLabel.scale_value_y**

Y-axis value.
[`scale_value_y`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationrail.navigationrail.MDNavigationRailItemLabel.scale_value_y) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailItemLabel.on__active**

Fired when the `_active` value changes.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailItem**

Implements a menu item with an icon and text.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`StateFocusBehavior`](https://kivymd.readthedocs.io/behaviors/focus/#kivymd.uix.behaviors.focus_behavior.StateFocusBehavior)
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
classes documentation.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailItem.active**

Is the element active.
[`active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationrail.navigationrail.MDNavigationRailItem.active) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailItem.radius**

Item radius.
Changed in version 2.0.0.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationrail.navigationrail.MDNavigationRailItem.radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [0, 0, 0, 0].

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailItem.on_active**

Fired when the [`active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationrail.navigationrail.MDNavigationRailItem.active) value changes.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailItem.on_enter**

Fired when mouse enter the bbox of the widget.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailItem.on_leave**

Fired when the mouse goes outside the widget border.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRailItem.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRail**

Navigation rail class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`RelativeLayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#kivy.uix.relativelayout.RelativeLayout)
classes documentation.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRail.radius**

Rail radius.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationrail.navigationrail.MDNavigationRail.radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [0, 0, 0, 0].

**kivymd.uix.navigationrail.navigationrail.MDNavigationRail.anchor**

The position of the panel with menu items.
Available options are: ‘top’, ‘bottom’, ‘center’.
[`anchor`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationrail.navigationrail.MDNavigationRail.anchor) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘center’.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRail.type**

Type of switching menu items.
Available options are: ‘labeled’, ‘selected’, ‘unselected’.
[`type`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationrail.navigationrail.MDNavigationRail.type) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘labeled’.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRail.fab_button**

**kivymd.uix.navigationrail.navigationrail.MDNavigationRail.menu_button**

**kivymd.uix.navigationrail.navigationrail.MDNavigationRail.on_size**

Fired when the application screen size changes.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRail.get_items**

Returns a list of [`MDNavigationRailItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.navigationrail.navigationrail.MDNavigationRailItem) objects.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRail.set_active_item**

Sets the active menu list item.

**kivymd.uix.navigationrail.navigationrail.MDNavigationRail.add_widget**

Add a new widget as a child of this widget.

---

## API - [`kivymd.uix.pickers.datepicker.datepicker`](https://kivymd.readthedocs.io/en/latest/components/datepicker/)

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker**

Implements the base class of the date picker.
Added in version 2.0.0.
For more information, see in the
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`MotionDatePickerBehavior`](https://kivymd.readthedocs.io/behaviors/motion/#kivymd.uix.behaviors.motion_behavior.MotionDatePickerBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout) and
classes documentation.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.day**

The day of the month to be opened by default. If not specified,
the current number will be used.
[`day`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.day) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.month**

The number of month to be opened by default. If not specified,
the current number will be used.
[`month`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.month) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.year**

The year of month to be opened by default. If not specified,
the current number will be used.
[`year`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.year) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.min_year**

The year of month to be opened by default. If not specified,
the current number will be used.
[`min_year`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.min_year) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 1914.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.max_year**

The year of month to be opened by default. If not specified,
the current number will be used.
[`max_year`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.max_year) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 2121.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.mode**

Dialog type.
Available options are: ‘picker’, ‘range’.
[`mode`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.mode) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to picker.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.min_date**

The minimum value of the date range for the ‘mode’ parameter.
Must be an object <class ‘datetime.date’>.
[`min_date`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.min_date) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.max_date**

The minimum value of the date range for the ‘mode’ parameter.
Must be an object <class ‘datetime.date’>.
[`max_date`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.max_date) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.radius**

Container radius.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [dp(16), dp(16), dp(16), dp(16)].

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.scrim_color**

Color for scrim in (r, g, b, a) or string format.
[`scrim_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.scrim_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to [0, 0, 0, 0.5].

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.supporting_text**

Supporting text.
[`supporting_text`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.supporting_text) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘Select date’.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.text_button_ok**

The text of the confirmation button.
[`text_button_ok`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.text_button_ok) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘Ok’.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.text_button_cancel**

The text of the cancel button.
[`text_button_cancel`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.text_button_cancel) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘Cancel’.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.mark_today**

Highlights the current day.
[`mark_today`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.mark_today) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.is_open**

Is the date picker dialog open.
[`is_open`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.is_open) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.sel_year**

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.sel_month**

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.sel_day**

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.calendar_layout**

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.get_date**

Returns a list of dates in the format
[datetime.date(yyyy, mm, dd), …].
The list has two dates if you use a date interval.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.set_text_full_date**

Returns a string like “Tue, Feb 2”.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.compare_date_range**

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.change_month**

Called when “chevron-left” and “chevron-right” buttons are pressed.
Switches the calendar to the previous/next month.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.generate_list_widgets_days**

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.update_calendar**

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.set_selected_widget**

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.restore_calendar_layout_properties**

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.set_calendar_layout_properties**

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.dismiss**

Dismiss the dialog date picker.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.open**

Show the dialog date picker.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.on_touch_down**

Receive a touch down event.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.on_select_day**

Fired when a day is selected.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.on_select_month**

Fired when a month is selected.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.on_select_year**

Fired when a year is selected.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.on_cancel**

Fired when the ‘Cancel’ button is pressed.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.on_ok**

Fired when the ‘Ok’ button is pressed.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.on_edit**

Fired when you click on the date editing icon.

**kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker.on_dismiss**

Fired when a date picker closes.

**kivymd.uix.pickers.datepicker.datepicker.MDDockedDatePicker**

Implements docked date picker.
Added in version 2.0.0.
For more information, see in the
[`CommonElevationBehavior`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior) and
[`MDBaseDatePicker`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker)
classes documentation.

**kivymd.uix.pickers.datepicker.datepicker.MDDockedDatePicker.generate_menu_month_year_selection**

Generates a list for the month or year selection menu.

**kivymd.uix.pickers.datepicker.datepicker.MDDockedDatePicker.open_close_menu_month_year_selection**

Hides the calendar layout and opens the list to select the month or
year.

**kivymd.uix.pickers.datepicker.datepicker.MDModalDatePicker**

Implements modal date picker.
Added in version 2.0.0.
For more information, see in the
[`CommonElevationBehavior`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior) and
[`MDBaseDatePicker`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker)
classes documentation.

**kivymd.uix.pickers.datepicker.datepicker.MDModalDatePicker.open**

Show the dialog date picker.

**kivymd.uix.pickers.datepicker.datepicker.MDModalDatePicker.generate_list_widgets_years**

**kivymd.uix.pickers.datepicker.datepicker.MDModalDatePicker.open_menu_year_selection**

**kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker**

Implements modal input date picker.
Added in version 2.0.0.
For more information, see in the
[`CommonElevationBehavior`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior) and
[`MDBaseDatePicker`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDBaseDatePicker)
classes documentation.

**kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker.date_format**

Format of date strings that will be entered.
Available options are: ‘dd/mm/yyyy’, ‘mm/dd/yyyy’, ‘yyyy/mm/dd’.
[`date_format`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker.date_format) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to None.

**kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker.default_input_date**

If true, the current date will be set in the input field.
[`default_input_date`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker.default_input_date) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker.error_text**

Error text when the date entered by the user is not valid.
[`error_text`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker.error_text) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘Invalid date format’.

**kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker.supporting_input_text**

Auxiliary text when entering the date manually.
[`supporting_input_text`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker.supporting_input_text) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘Enter date’.

**kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker.generate_list_widgets_days**

**kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker.update_calendar**

**kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker.set_input_date**

**kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker.get_date**

Returns a list of dates in the format
[datetime.date(yyyy, mm, dd), …].
The list has two dates if you use a date interval.

**kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker.get_current_date_from_format**

Returns the date according to the set format in [`date_format`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker.date_format).

**kivymd.uix.pickers.datepicker.datepicker.MDModalInputDatePicker.open**

Show the dialog date picker.

---

## API - [`kivymd.uix.pickers.timepicker.timepicker`](https://kivymd.readthedocs.io/en/latest/components/timepicker/)

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker**

Implements the base class of the time picker.
Added in version 2.0.0.
For more information, see in the
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`MotionTimePickerBehavior`](https://kivymd.readthedocs.io/behaviors/motion/#kivymd.uix.behaviors.motion_behavior.MotionTimePickerBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout) and
classes documentation.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.hour**

Current hour.
[`hour`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.hour) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘12’.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.minute**

Current minute.
[`minute`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.minute) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to 0.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.am_pm**

Current AM/PM mode.
[`am_pm`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.am_pm) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘am’.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.animation_duration**

Duration of the animations.
[`animation_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.animation_duration) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.animation_transition**

Transition type of the animations.
[`animation_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.animation_transition) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘out_quad’.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.time**

Returns the current time object.
[`time`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.time) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.headline_text**

Headline text.
[`headline_text`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.headline_text) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘Select time’.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.text_button_ok**

The text of the confirmation button.
[`text_button_ok`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.text_button_ok) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘Ok’.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.text_button_cancel**

The text of the cancel button.
[`text_button_cancel`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.text_button_cancel) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘Cancel’.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.radius**

Container radius.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [dp(16), dp(16), dp(16), dp(16)].

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.is_open**

Is the date picker dialog open.
[`is_open`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.is_open) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.scrim_color**

Color for scrim in (r, g, b, a) or string format.
[`scrim_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.scrim_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to [0, 0, 0, 0.5].

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.set_time**

Manually set time dialog with the specified time.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.open**

Show the dialog time picker.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.on_touch_down**

Receive a touch down event.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.dismiss**

Dismiss the dialog time picker.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.on_dismiss**

Fired when a time picker closes.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.on_cancel**

Fired when the ‘Cancel’ button is pressed.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.on_ok**

Fired when the ‘Ok’ button is pressed.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.on_hour_select**

Fired when the hour input field container is clicked.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.on_minute_select**

Fired when the minute input field container is clicked.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.on_am_pm**

Fired when the AP/PM switching elements are pressed.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.on_edit**

Fired when you click on the time editing icon.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.on_selector_hour**

Fired when switching the hour value in the clock face container.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.on_selector_minute**

Fired when switching the minute value in the clock face container.

**kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker.on_time_input**

Fired when switching the minute value in the clock face container.

**kivymd.uix.pickers.timepicker.timepicker.MDTimePickerInput**

Implements input time picker.
Added in version 2.0.0.
For more information, see in the
[`CommonElevationBehavior`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior) and
[`MDBaseTimePicker`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker)
classes documentation.

**kivymd.uix.pickers.timepicker.timepicker.MDTimePickerDialVertical**

Implements vertical time picker.
Added in version 2.0.0.
For more information, see in the
[`CommonElevationBehavior`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior) and
[`MDBaseTimePicker`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker)
classes documentation.

**kivymd.uix.pickers.timepicker.timepicker.MDTimePickerDialHorizontal**

Implements horizontal time picker.
Added in version 2.0.0.
For more information, see in the
[`CommonElevationBehavior`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior) and
[`MDBaseTimePicker`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.pickers.timepicker.timepicker.MDBaseTimePicker)
classes documentation.

---

## API - [`kivymd.uix.progressindicator.progressindicator`](https://kivymd.readthedocs.io/en/latest/components/progressindicator/)

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator**

Implementation of the linear progress indicator.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`ProgressBar`](https://kivy.org/doc/stable/api-kivy.uix.progressbar.html#kivy.uix.progressbar.ProgressBar)
classes documentation.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.radius**

Progress line radius.
Added in version 1.2.0.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [0, 0, 0, 0].

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.reversed**

Reverse the direction the progressbar moves.
[`reversed`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.reversed) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.orientation**

Orientation of progressbar. Available options are: ‘horizontal ‘,
‘vertical’.
[`orientation`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.orientation) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘horizontal’.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.indicator_color**

Color of the active track.
Changed in version 2.0.0:Rename from color to indicator_color attribute.
[`indicator_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.indicator_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.track_color**

Progress bar back color in (r, g, b, a) or string format.
Added in version 1.0.0.
Changed in version 2.0.0:Rename from back_color to track_color attribute.
[`track_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.track_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.running_determinate_transition**

Running transition.
Changed in version 2.0.0:Rename from running_transition to running_determinate_transition
attribute.
[`running_determinate_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.running_determinate_transition) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘out_quart’.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.catching_determinate_transition**

Catching transition.
Changed in version 2.0.0:Rename from catching_transition to catching_determinate_transition
attribute.
[`catching_determinate_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.catching_determinate_transition) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘out_quart’.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.running_determinate_duration**

Running duration.
Changed in version 2.0.0:Rename from running_duration to running_determinate_duration
attribute.
[`running_determinate_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.running_determinate_duration) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 2.5.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.catching_determinate_duration**

Catching duration.
`running_duration` is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.8.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.type**

Type of progressbar. Available options are: ‘indeterminate ‘,
‘determinate’.
[`type`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.type) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to None.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.running_indeterminate_transition**

Running transition.
[`running_indeterminate_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.running_indeterminate_transition) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘in_cubic’.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.catching_indeterminate_transition**

Catching transition.
[`catching_indeterminate_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.catching_indeterminate_transition) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘out_quart’.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.running_indeterminate_duration**

Running duration.
[`running_indeterminate_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.running_indeterminate_duration) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.5.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.catching_indeterminate_duration**

Catching duration.
[`catching_indeterminate_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.catching_indeterminate_duration) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.8.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.check_size**

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.start**

Start animation.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.stop**

Stop animation.

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.running_away**

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.catching_up**

**kivymd.uix.progressindicator.progressindicator.MDLinearProgressIndicator.on_value**

**kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator**

Implementation of the circular progress indicator.
Changed in version 2.0.0:Rename MDSpinner to MDCircularProgressIndicator class.
For more information, see in the
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
classes documentation.
It can be used either as an indeterminate indicator that loops while
the user waits for something to happen, or as a determinate indicator.
Set [`determinate`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.determinate) to **True** to activate determinate mode, and
[`determinate_time`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.determinate_time) to set the duration of the animation.

**kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.determinate**

Determinate value.
[`determinate`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.determinate) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.determinate_time**

Determinate time value.
[`determinate_time`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.determinate_time) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 2.

**kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.line_width**

Progress line width of indicator.
[`line_width`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.line_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to dp(2.25).

**kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.active**

Use [`active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.active) to start or stop the indicator.
[`active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.active) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.color**

Indicator color in (r, g, b, a) or string format.
[`color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.palette**

A set of colors. Changes with each completed indicator cycle.
[`palette`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.palette) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [].

**kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.on__rotation_angle**

**kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.on_palette**

Fired when the palette value changes.

**kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.on_active**

Fired when the active value changes.

**kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.on_determinate_complete**

The event is fired at the end of the indicator loop in the
determinate = True mode.

**kivymd.uix.progressindicator.progressindicator.MDCircularProgressIndicator.check_determinate**

Fired when the class is initialized.

---

## API - [`kivymd.uix.recycleboxlayout`](https://kivymd.readthedocs.io/en/latest/components/mdrecycleboxlayout/)

**kivymd.uix.recycleboxlayout.MDRecycleBoxLayout**

Recycle box layout class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`RecycleBoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.recycleboxlayout.html#kivy.uix.recycleboxlayout.RecycleBoxLayout) and
[`MDAdaptiveWidget`](https://kivymd.readthedocs.io/api/kivymd/uix/#kivymd.uix.MDAdaptiveWidget)
classes documentation.

---

## API - [`kivymd.uix.recyclegridlayout`](https://kivymd.readthedocs.io/en/latest/components/recyclegridlayout/)

**kivymd.uix.recyclegridlayout.MDRecycleGridLayout**

Recycle grid layout class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`RecycleGridLayout`](https://kivy.org/doc/stable/api-kivy.uix.recyclegridlayout.html#kivy.uix.recyclegridlayout.RecycleGridLayout) and
[`MDAdaptiveWidget`](https://kivymd.readthedocs.io/api/kivymd/uix/#kivymd.uix.MDAdaptiveWidget)
classes documentation.

---

## API - [`kivymd.uix.recycleview`](https://kivymd.readthedocs.io/en/latest/components/recycleview/)

**kivymd.uix.recycleview.MDRecycleView**

Recycle view class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`RecycleView`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.html#kivy.uix.recycleview.RecycleView) and
[`MDAdaptiveWidget`](https://kivymd.readthedocs.io/api/kivymd/uix/#kivymd.uix.MDAdaptiveWidget)
classes documentation.

---

## API - [`kivymd.uix.refreshlayout.refreshlayout`](https://kivymd.readthedocs.io/en/latest/components/refreshlayout/)

**kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout**

Refresh layout class.
For more information, see in the
[`MDScrollView`](https://kivymd.readthedocs.io/en/scrollview/#kivymd.uix.scrollview.MDScrollView) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) class documentation.

**kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.root_layout**

The spinner will be attached to this layout.
[`root_layout`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.root_layout) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.refresh_callback**

The method that will be called at the on_touch_up event,
provided that the overscroll of the list has been registered.
[`refresh_callback`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.refresh_callback) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.spinner_color**

Color of the spinner in (r, g, b, a) or string format.
Added in version 1.2.0.
[`spinner_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.spinner_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to [1, 1, 1, 1].

**kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.circle_color**

Color of the ellipse around the spinner in (r, g, b, a) or string format.
Added in version 1.2.0.
[`circle_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.circle_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.show_transition**

Transition of the spinner’s opening.
Added in version 1.2.0.
[`show_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.show_transition) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘out_elastic’.

**kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.show_duration**

Duration of the spinner display.
Added in version 1.2.0.
[`show_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.show_duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.8.

**kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.hide_transition**

Transition of hiding the spinner.
Added in version 1.2.0.
[`hide_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.hide_transition) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘out_elastic’.

**kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.hide_duration**

Duration of hiding the spinner.
Added in version 1.2.0.
[`hide_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.hide_duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.8.

**kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See `on_touch_down()` for more information.

**kivymd.uix.refreshlayout.refreshlayout.MDScrollViewRefreshLayout.refresh_done**

---

## API - [`kivymd.uix.relativelayout`](https://kivymd.readthedocs.io/en/latest/components/relativelayout/)

**kivymd.uix.relativelayout.MDRelativeLayout**

Relative layout class.
For more information see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`RelativeLayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#kivy.uix.relativelayout.RelativeLayout) and
[`MDAdaptiveWidget`](https://kivymd.readthedocs.io/api/kivymd/uix/#kivymd.uix.MDAdaptiveWidget)
classes documentation.

---

## API - [`kivymd.uix.responsivelayout`](https://kivymd.readthedocs.io/en/latest/components/responsivelayout/)

**kivymd.uix.responsivelayout.MDResponsiveLayout**

**kivymd.uix.responsivelayout.MDResponsiveLayout.mobile_view**

Mobile view. Must be a Kivy or KivyMD widget.
[`mobile_view`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.responsivelayout.MDResponsiveLayout.mobile_view) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivymd.uix.responsivelayout.MDResponsiveLayout.tablet_view**

Tablet view. Must be a Kivy or KivyMD widget.
[`tablet_view`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.responsivelayout.MDResponsiveLayout.tablet_view) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivymd.uix.responsivelayout.MDResponsiveLayout.desktop_view**

Desktop view. Must be a Kivy or KivyMD widget.
[`desktop_view`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.responsivelayout.MDResponsiveLayout.desktop_view) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivymd.uix.responsivelayout.MDResponsiveLayout.on_change_screen_type**

Called when the screen type changes.

**kivymd.uix.responsivelayout.MDResponsiveLayout.on_size**

Called when the application screen size changes.

**kivymd.uix.responsivelayout.MDResponsiveLayout.set_screen**

Sets the screen according to the type of application screen size:
mobile/tablet or desktop view.

---

## API - [`kivymd.uix.screen`](https://kivymd.readthedocs.io/en/latest/components/screen/)

**kivymd.uix.screen.MDScreen**

Screen is an element intended to be used with a
[`MDScreenManager`](https://kivymd.readthedocs.io/en/screenmanager/#kivymd.uix.screenmanager.MDScreenManager).
For more information see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`Screen`](https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html#kivy.uix.screenmanager.Screen) and
[`MDAdaptiveWidget`](https://kivymd.readthedocs.io/api/kivymd/uix/#kivymd.uix.MDAdaptiveWidget)
classes documentation.

**kivymd.uix.screen.MDScreen.hero_to**

Must be a [`MDHeroTo`](https://kivymd.readthedocs.io/en/hero/#kivymd.uix.hero.MDHeroTo) class.
See the documentation of the
[MDHeroTo](https://kivymd.readthedocs.io/en/latest/components/hero/)
widget for more detailed information.
Deprecated since version 1.0.0:Use attr:heroes_to attribute instead.
[`hero_to`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.screen.MDScreen.hero_to) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivymd.uix.screen.MDScreen.heroes_to**

Must be a list of [`MDHeroTo`](https://kivymd.readthedocs.io/en/hero/#kivymd.uix.hero.MDHeroTo) class.
Added in version 1.0.0.
[`heroes_to`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.screen.MDScreen.heroes_to) is an `LiatProperty`
and defaults to [].

**kivymd.uix.screen.MDScreen.on_hero_to**

Fired when the value of the [`hero_to`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.screen.MDScreen.hero_to) attribute changes.

---

## API - [`kivymd.uix.screenmanager`](https://kivymd.readthedocs.io/en/latest/components/screenmanager/)

**kivymd.uix.screenmanager.MDScreenManager**

Screen manager. This is the main class that will control your
[`MDScreen`](https://kivymd.readthedocs.io/en/screen/#kivymd.uix.screen.MDScreen) stack and memory.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`ScreenManager`](https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html#kivy.uix.screenmanager.ScreenManager) and
[`MDAdaptiveWidget`](https://kivymd.readthedocs.io/api/kivymd/uix/#kivymd.uix.MDAdaptiveWidget)
classes documentation.

**kivymd.uix.screenmanager.MDScreenManager.current_hero**

The name of the current tag for the [`MDHeroFrom`](https://kivymd.readthedocs.io/en/hero/#kivymd.uix.hero.MDHeroFrom)
and [`MDHeroTo`](https://kivymd.readthedocs.io/en/hero/#kivymd.uix.hero.MDHeroTo) objects that will be animated when
animating the transition between screens.
Deprecated since version 1.1.0:Use [`current_heroes`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.screenmanager.MDScreenManager.current_heroes) attribute instead.
See the [Hero](https://kivymd.readthedocs.io/en/latest/components/hero/)
module documentation for more information about creating and using Hero
animations.
[`current_hero`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.screenmanager.MDScreenManager.current_hero) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to None.

**kivymd.uix.screenmanager.MDScreenManager.current_heroes**

A list of names (tags) of heroes that need to be animated when moving
to the next screen.
Added in version 1.1.0.
[`current_heroes`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.screenmanager.MDScreenManager.current_heroes) is an [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [].

**kivymd.uix.screenmanager.MDScreenManager.check_transition**

Sets the default type transition.

**kivymd.uix.screenmanager.MDScreenManager.get_hero_from_widget**

Get a list of [`MDHeroFrom`](https://kivymd.readthedocs.io/en/hero/#kivymd.uix.hero.MDHeroFrom) objects according
to the tag names specified in the [`current_heroes`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.screenmanager.MDScreenManager.current_heroes) list.

**kivymd.uix.screenmanager.MDScreenManager.on_current_hero**

Fired when the value of the [`current_hero`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.screenmanager.MDScreenManager.current_hero) attribute changes.

**kivymd.uix.screenmanager.MDScreenManager.add_widget**

Changed in version 2.1.0:Renamed argument screen to widget.

---

## API - [`kivymd.uix.scrollview`](https://kivymd.readthedocs.io/en/latest/components/scrollview/)

**kivymd.uix.scrollview.StretchOverScrollStencil**

Stretches the view on overscroll and absorbs
velocity at start and end to convert to stretch.
Added in version 2.0.0.

If you need any documentation please look at
`dampedscrolleffect`.

**kivymd.uix.scrollview.StretchOverScrollStencil.minimum_absorbed_velocity**

**kivymd.uix.scrollview.StretchOverScrollStencil.maximum_velocity**

**kivymd.uix.scrollview.StretchOverScrollStencil.stretch_intensity**

**kivymd.uix.scrollview.StretchOverScrollStencil.exponential_scalar**

**kivymd.uix.scrollview.StretchOverScrollStencil.scroll_friction**

**kivymd.uix.scrollview.StretchOverScrollStencil.approx_normailzer**

**kivymd.uix.scrollview.StretchOverScrollStencil.duration_normailzer**

**kivymd.uix.scrollview.StretchOverScrollStencil.scroll_view**

**kivymd.uix.scrollview.StretchOverScrollStencil.scroll_scale**

**kivymd.uix.scrollview.StretchOverScrollStencil.scale_axis**

**kivymd.uix.scrollview.StretchOverScrollStencil.last_touch_pos**

**kivymd.uix.scrollview.StretchOverScrollStencil.clamp**

**kivymd.uix.scrollview.StretchOverScrollStencil.is_top_or_bottom**

**kivymd.uix.scrollview.StretchOverScrollStencil.on_value**

**kivymd.uix.scrollview.StretchOverScrollStencil.get_hw**

**kivymd.uix.scrollview.StretchOverScrollStencil.set_scale_origin**

**kivymd.uix.scrollview.StretchOverScrollStencil.absorb_impact**

**kivymd.uix.scrollview.StretchOverScrollStencil.get_component**

**kivymd.uix.scrollview.StretchOverScrollStencil.can_stretch_touch**

**kivymd.uix.scrollview.StretchOverScrollStencil.convert_overscroll**

**kivymd.uix.scrollview.StretchOverScrollStencil.reset_scale**

**kivymd.uix.scrollview.StretchOverScrollBehavior**

Shared overscroll-stretch setup for ScrollView-based widgets.

**kivymd.uix.scrollview.StretchOverScrollBehavior.on_touch_down**

**kivymd.uix.scrollview.StretchOverScrollBehavior.on_touch_move**

**kivymd.uix.scrollview.StretchOverScrollBehavior.on_touch_up**

**kivymd.uix.scrollview.MDScrollView**

An approximate implementation to Material Design’s overscorll effect.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`ScrollView`](https://kivy.org/doc/stable/api-kivy.uix.scrollview.html#kivy.uix.scrollview.ScrollView)
classes documentation.

---

## API - [`kivymd.uix.search.search`](https://kivymd.readthedocs.io/en/latest/components/search/)

**kivymd.uix.search.search.MDSearchTrailingAvatar**

Trailing avatar class.
For more information, see in the
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.button.html#kivy.uix.behaviors.button.ButtonBehavior) and
[`Image`](https://kivy.org/doc/stable/api-kivy.uix.image.html#kivy.uix.image.Image)
classes documentation.

**kivymd.uix.search.search.MDSearchLeadingIcon**

Leading icon class.
For more information, see in the
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.button.html#kivy.uix.behaviors.button.ButtonBehavior) and
`MDIcon`
classes documentation.

**kivymd.uix.search.search.MDSearchTrailingIcon**

Trailing icon class.
For more information, see in the
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.button.html#kivy.uix.behaviors.button.ButtonBehavior) and
`MDIcon`
classes documentation.

**kivymd.uix.search.search.MDSearchBarTrailingContainer**

Trailing container class for search bar.
For more information, see in the
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
class documentation.

**kivymd.uix.search.search.MDSearchBarLeadingContainer**

Leading container class for search bar.
For more information, see in the
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
class documentation.

**kivymd.uix.search.search.MDSearchViewTrailingContainer**

Trailing container class for search view.
For more information, see in the
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
class documentation.

**kivymd.uix.search.search.MDSearchViewLeadingContainer**

Leading container class for search view.
For more information, see in the
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
class documentation.

**kivymd.uix.search.search.MDSearchViewContainer**

A container for widgets that are displayed when the search bar is in focus.
For more information, see in the
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
class documentation.

**kivymd.uix.search.search.MDSearchViewContainer.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.search.search.MDSearchViewContainer.show_child**

Displays the stored child widget with a fade-in animation.

**kivymd.uix.search.search.MDSearchViewContainer.hide_child**

Removes the stored child widget from the layout.

**kivymd.uix.search.search.MDSearchViewContainer.remove_widget**

Remove a widget from the children of this widget.

**kivymd.uix.search.search.MDSearchBar**

Search bar class.
For more information, see in the
[`Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
class documentation.

**kivymd.uix.search.search.MDSearchBar.leading_icon**

Leading icon name.
[`leading_icon`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.search.search.MDSearchBar.leading_icon) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘magnify’.

**kivymd.uix.search.search.MDSearchBar.supporting_text**

Supporting text.
[`supporting_text`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.search.search.MDSearchBar.supporting_text) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘Hinted search text’.

**kivymd.uix.search.search.MDSearchBar.view_root**

Root widget for search view.
[`view_root`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.search.search.MDSearchBar.view_root) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivymd.uix.search.search.MDSearchBar.docked_width**

Docked width.
[`docked_width`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.search.search.MDSearchBar.docked_width) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to dp(360).

**kivymd.uix.search.search.MDSearchBar.docked_height**

Docked height.
[`docked_height`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.search.search.MDSearchBar.docked_height) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to dp(240).

**kivymd.uix.search.search.MDSearchBar.docked**

If True, the search bar will be docked.
[`docked`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.search.search.MDSearchBar.docked) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.search.search.MDSearchBar.text**

Search query text.
[`text`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.search.search.MDSearchBar.text) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘’.

**kivymd.uix.search.search.MDSearchBar.on_docked**

Called when the [`docked`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.search.search.MDSearchBar.docked) property changes.

Updates the size_hint_x and width accordingly. When docked,
sets a fixed width using docked_width property.

**kivymd.uix.search.search.MDSearchBar.on_supporting_text**

Called when the [`supporting_text`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.search.search.MDSearchBar.supporting_text) property changes.

Updates the hint text of the text input field to display
the provided supporting text.

**kivymd.uix.search.search.MDSearchBar.on_view_root**

Called when the view_root property changes.

Removes the search widget from its current parent (if any),
adds it to the new view_root, and initializes the search widget
state and position.

**kivymd.uix.search.search.MDSearchBar.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.search.search.MDSearchBar.close_view**

Closes the search view.

**kivymd.uix.search.search.MDSearchBar.open_view**

Opens the search view.

**kivymd.uix.search.search.MDSearchBar.on_open**

Event handler for the on_open event.
Override this method in subclasses to handle the search view
opening event.

**kivymd.uix.search.search.MDSearchBar.on_close**

Event handler for the on_close event.
Override this method in subclasses to handle the search view
closing event.

**kivymd.uix.search.search.MDSearchBar.on_text**

Called when the [`text`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.search.search.MDSearchBar.text) property changes.

Updates the text in the text input field to match the new text
property value.

---

## API - [`kivymd.uix.segmentedbutton.segmentedbutton`](https://kivymd.readthedocs.io/en/latest/components/segmentedbutton/)

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButtonItem**

Segment button item.
For more information see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`RectangularRippleBehavior`](https://kivymd.readthedocs.io/behaviors/ripple/#id0) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
[`StateLayerBehavior`](https://kivymd.readthedocs.io/behaviors/state-layer/#kivymd.uix.behaviors.state_layer_behavior.StateLayerBehavior) and
[`RelativeLayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#kivy.uix.relativelayout.RelativeLayout) and
class documentation.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButtonItem.selected_color**

Color of the marked segment.
Added in version 2.0.0.
[`selected_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButtonItem.selected_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButtonItem.md_bg_color_disabled**

The background color in (r, g, b, a) or string format of the list item when
the list item is disabled.
[`md_bg_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButtonItem.md_bg_color_disabled) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButtonItem.active**

Background color of an disabled segment.
[`active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButtonItem.active) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButtonItem.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButtonItem.on_line_color**

Fired when the values of `line_color` change.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButtonItem.on_active**

Fired when the [`active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButtonItem.active) value changes.
Animates the marker icon for the element.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButtonItem.on_disabled**

Fired when the `disabled` value changes.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton**

Segment button panel.
For more information, see in the
[`MDBoxLayout`](https://kivymd.readthedocs.io/en/boxlayout/#kivymd.uix.boxlayout.MDBoxLayout) class documentation.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.multiselect**

Do I allow multiple segment selection.
[`multiselect`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.multiselect) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.hiding_icon_transition**

Name of the transition hiding the current icon.
[`hiding_icon_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.hiding_icon_transition) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘linear’.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.hiding_icon_duration**

Duration of hiding the current icon.
[`hiding_icon_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.hiding_icon_duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 1.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.opening_icon_transition**

The name of the transition that opens a new icon of the “marked” type.
[`opening_icon_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.opening_icon_transition) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘linear’.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.opening_icon_duration**

The duration of opening a new icon of the “marked” type.
[`opening_icon_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.opening_icon_duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.1.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.selected_segments**

The list of [`MDSegmentedButtonItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButtonItem) objects that are currently
marked.
[`selected_segments`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.selected_segments) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [].

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.type**

Density can be used in denser UIs where space is limited.
Density is only applied to the height. Each step down in density removes
‘4dp’ from the height.
Added in version 2.0.0.
Available options are: ‘large’, ‘normal’, ‘medium’, ‘small’.
[`type`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.type) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘large’.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.selected_icon_color**

Color in (r, g, b, a) or string format of the icon of the marked segment.
Added in version 2.0.0.
[`selected_icon_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.selected_icon_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.get_marked_items**

Returns a list of active item objects.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.get_items**

Returns a list of item objects.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.adjust_segment_radius**

Rounds off the first and last elements.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.mark_item**

Fired when a segment element is clicked (on_release event).

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButton.remove_widget**

Remove a widget from the children of this widget.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentButtonIcon**

Implements a icon for [`MDSegmentedButtonItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButtonItem) class.
Added in version 2.0.0.
For more information, see in the
[`MDIcon`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDIcon) class documentation.

**kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentButtonLabel**

Implements a label for [`MDSegmentedButtonItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.segmentedbutton.segmentedbutton.MDSegmentedButtonItem) class.
Added in version 2.0.0.
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) class documentation.

---

## API - [`kivymd.uix.selectioncontrol.selectioncontrol`](https://kivymd.readthedocs.io/en/latest/components/selectioncontrols/)

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox**

Checkbox class.
For more information, see in the
[`StateLayerBehavior`](https://kivymd.readthedocs.io/behaviors/state-layer/#kivymd.uix.behaviors.state_layer_behavior.StateLayerBehavior) and
[`CircularRippleBehavior`](https://kivymd.readthedocs.io/behaviors/ripple/#id1) and
[`ScaleBehavior`](https://kivymd.readthedocs.io/behaviors/scale/#kivymd.uix.behaviors.scale_behavior.ScaleBehavior) and
[`ToggleButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ToggleButtonBehavior) and
[`MDIcon`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDIcon)
classes documentation.

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.checkbox_icon_normal**

Background icon of the checkbox used for the default graphical
representation when the checkbox is not pressed.
[`checkbox_icon_normal`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.checkbox_icon_normal) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘checkbox-blank-outline’.

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.checkbox_icon_down**

Background icon of the checkbox used for the default graphical
representation when the checkbox is pressed.
[`checkbox_icon_down`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.checkbox_icon_down) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘checkbox-marked’.

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.radio_icon_normal**

Background icon (when using the group option) of the checkbox used for
the default graphical representation when the checkbox is not pressed.
[`radio_icon_normal`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.radio_icon_normal) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘checkbox-blank-circle-outline’.

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.radio_icon_down**

Background icon (when using the group option) of the checkbox used for
the default graphical representation when the checkbox is pressed.
[`radio_icon_down`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.radio_icon_down) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘checkbox-marked-circle’.

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.color_active**

Color in (r, g, b, a) or string format when the checkbox is in the active state.
Added in version 1.0.0.

[`color_active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.color_active) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.color_inactive**

Color in (r, g, b, a) or string format when the checkbox is in the inactive state.
Added in version 1.0.0.

[`color_inactive`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.color_inactive) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.color_disabled**

Color in (r, g, b, a) or string format when the checkbox is in the disabled state.
Added in version 2.0.0:Use [`color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.color_disabled) instead.
[`color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.color_disabled) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.disabled_color**

Color in (r, g, b, a) or string format when the checkbox is in the disabled state.
Deprecated since version 2.0.0:Use [`color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.color_disabled) instead.
[`disabled_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.disabled_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.selected_color**

Color in (r, g, b, a) or string format when the checkbox is in the active state.
Deprecated since version 1.0.0:Use [`color_active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.color_active) instead.
[`selected_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.selected_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.unselected_color**

Color in (r, g, b, a) or string format when the checkbox is in the inactive state.
Deprecated since version 1.0.0:Use [`color_inactive`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.color_inactive) instead.
[`unselected_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.unselected_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.disable_animation**

Disable the checkbox animation.
Added in version 2.0.0.

[`disable_animation`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.disable_animation) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.update_icon**

Fired when the values of
[`checkbox_icon_normal`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.checkbox_icon_normal) and
[`checkbox_icon_down`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.checkbox_icon_down) and
[`radio_icon_normal`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.radio_icon_normal) and
`group`
change.

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.set_root_active**

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.set_child_active**

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.on_state**

Fired when the values of `state` change.

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.on_active**

Fired when the values of `active` change.

**kivymd.uix.selectioncontrol.selectioncontrol.MDCheckbox.on_touch_down**

Receive a touch down event.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch**

Switch class.
For more information, see in the
[`StateLayerBehavior`](https://kivymd.readthedocs.io/behaviors/state-layer/#kivymd.uix.behaviors.state_layer_behavior.StateLayerBehavior) and
[`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.ButtonBehavior) and
[`MDFloatLayout`](https://kivymd.readthedocs.io/en/floatlayout/#kivymd.uix.floatlayout.MDFloatLayout)
classes documentation.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.width**

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.height**

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.md_bg_color_disabled**

The background color in (r, g, b, a) or string format of the switch when
the switch is disabled.
[`md_bg_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.md_bg_color_disabled) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.ripple_effect**

Allows or does not allow the ripple effect when activating/deactivating
the switch.
Added in version 2.0.0.
[`ripple_effect`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.ripple_effect) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.icon_active**

Thumb icon when the switch is in the active state (only M3 style).
Added in version 1.0.0.

[`icon_active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.icon_active) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘’.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.icon_inactive**

Thumb icon when the switch is in an inactive state (only M3 style).
Added in version 1.0.0.

[`icon_inactive`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.icon_inactive) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘’.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.icon_active_color**

Thumb icon color in (r, g, b, a) or string format when the switch is in the
active state (only M3 style).
Added in version 1.0.0.

[`icon_active_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.icon_active_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.icon_inactive_color**

Thumb icon color in (r, g, b, a) or string format when the switch is in an
inactive state (only M3 style).
Added in version 1.0.0.

[`icon_inactive_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.icon_inactive_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.thumb_color_active**

The color in (r, g, b, a) or string format of the thumb when the switch is active.
Added in version 1.0.0.

[`thumb_color_active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.thumb_color_active) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and default to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.thumb_color_inactive**

The color in (r, g, b, a) or string format of the thumb when the switch is inactive.
Added in version 1.0.0.

[`thumb_color_inactive`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.thumb_color_inactive) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and default to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.thumb_color_disabled**

The color in (r, g, b, a) or string format of the thumb when the switch is
in the disabled state.

[`thumb_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.thumb_color_disabled) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and default to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.track_color_active**

The color in (r, g, b, a) or string format of the track when the switch is active.

[`track_color_active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.track_color_active) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and default to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.track_color_inactive**

The color in (r, g, b, a) or string format of the track when the switch is inactive.
Added in version 1.0.0.

[`track_color_inactive`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.track_color_inactive) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and default to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.track_color_disabled**

The color in (r, g, b, a) or string format of the track when the switch is
in the disabled state.

[`track_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.track_color_disabled) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and default to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.line_color_disabled**

The color of the outline in the disabled state
Added in version 2.0.0.
[`line_color_disabled`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.line_color_disabled) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.disable_animation**

Disable the switch animation.
Added in version 2.0.0.

[`disable_animation`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.disable_animation) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.set_icon**

Fired when the values of
[`icon_active`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.icon_active) and [`icon_inactive`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.icon_inactive) change.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.on_line_color**

Fired when the values of `line_color` change.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.on_ripple_effect**

Fired when the values of [`ripple_effect`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.ripple_effect) change.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.on_active**

Fired when the values of `active` change.

**kivymd.uix.selectioncontrol.selectioncontrol.MDSwitch.on_thumb_down**

Fired at the on_touch_down event of the `Thumb` object.
Indicates the state of the switch “on/off” by an animation of
increasing the size of the thumb.

---

## API - [`kivymd.uix.slider.slider`](https://kivymd.readthedocs.io/en/latest/components/slider/)

**kivymd.uix.slider.slider.MDSlider**

Slider class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`Slider`](https://kivy.org/doc/stable/api-kivy.uix.slider.html#kivy.uix.slider.Slider)
classes documentation.

**kivymd.uix.slider.slider.MDSlider.track_active_width**

Width of the active track.
Added in version 2.0.0.
[`track_active_width`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSlider.track_active_width) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to dp(4).

**kivymd.uix.slider.slider.MDSlider.track_inactive_width**

Width of the inactive track.
Added in version 2.0.0.
[`track_inactive_width`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSlider.track_inactive_width) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to dp(4).

**kivymd.uix.slider.slider.MDSlider.step_point_size**

Step point size.
Added in version 2.0.0.
[`step_point_size`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSlider.step_point_size) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to dp(1).

**kivymd.uix.slider.slider.MDSlider.track_active_color**

Color of the active track.
Added in version 2.0.0.
Changed in version 2.0.0:Rename from track_color_active to track_active_color
[`track_active_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSlider.track_active_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.slider.slider.MDSlider.track_active_step_point_color**

Color of step points on active track.
Added in version 2.0.0.
[`track_active_step_point_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSlider.track_active_step_point_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.slider.slider.MDSlider.track_inactive_step_point_color**

Color of step points on inactive track.
Added in version 2.0.0.
[`track_inactive_step_point_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSlider.track_inactive_step_point_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.slider.slider.MDSlider.track_inactive_color**

Color of the inactive track.
Added in version 2.0.0.
Changed in version 2.0.0:Rename from track_color_inactive to track_inactive_color
[`track_active_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSlider.track_active_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.slider.slider.MDSlider.value_container_show_anim_duration**

Duration of the animation opening of the label value.
Added in version 2.0.0.
[`value_container_show_anim_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSlider.value_container_show_anim_duration) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivymd.uix.slider.slider.MDSlider.value_container_hide_anim_duration**

Duration of closing the animation of the label value.
Added in version 2.0.0.
[`value_container_hide_anim_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSlider.value_container_hide_anim_duration) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivymd.uix.slider.slider.MDSlider.value_container_show_anim_transition**

The type of the opening animation of the label value.
Added in version 2.0.0.
[`value_container_show_anim_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSlider.value_container_show_anim_transition) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘out_circ’.

**kivymd.uix.slider.slider.MDSlider.value_container_hide_anim_transition**

The type of the closing animation of the label value.
Added in version 2.0.0.
[`value_container_hide_anim_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSlider.value_container_hide_anim_transition) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘out_circ’.

**kivymd.uix.slider.slider.MDSlider.handle_anim_transition**

Handle animation type.
Added in version 2.0.0.
[`handle_anim_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSlider.handle_anim_transition) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘out_circ’.

**kivymd.uix.slider.slider.MDSlider.handle_anim_duration**

Handle animation duration.
Added in version 2.0.0.
[`handle_anim_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSlider.handle_anim_duration) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivymd.uix.slider.slider.MDSlider.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.slider.slider.MDSlider.update_points**

Draws the step points on the slider.

**kivymd.uix.slider.slider.MDSlider.on_size**

Fired when the widget is resized.

**kivymd.uix.slider.slider.MDSlider.on_touch_down**

Receive a touch down event.

**kivymd.uix.slider.slider.MDSlider.on_value_pos**

Fired when the value_pos value changes.
Sets a new value for the value label texture.

**kivymd.uix.slider.slider.MDSlider.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSlider.on_touch_down) for more information.

**kivymd.uix.slider.slider.MDSlider.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSlider.on_touch_down) for more information.

**kivymd.uix.slider.slider.MDSlider.on_handle_enter**

Scales the container of the label value.

**kivymd.uix.slider.slider.MDSlider.on_handle_leave**

Scales the container of the label value.

**kivymd.uix.slider.slider.MDSliderHandle**

Handle class.
Added in version 2.0.0.
For more information, see in the
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`StateFocusBehavior`](https://kivymd.readthedocs.io/behaviors/focus/#kivymd.uix.behaviors.focus_behavior.StateFocusBehavior) and
[`Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
classes documentation.

**kivymd.uix.slider.slider.MDSliderHandle.radius**

Handle radius.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSliderHandle.radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [dp(10), dp(10), dp(10), dp(10)].

**kivymd.uix.slider.slider.MDSliderHandle.size**

Handle size.
[`size`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSliderHandle.size) is an [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [dp(20), dp(20)].

**kivymd.uix.slider.slider.MDSliderHandle.state_layer_size**

Handle state layer size.
[`state_layer_size`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSliderHandle.state_layer_size) is an [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [dp(40), dp(40)].

**kivymd.uix.slider.slider.MDSliderHandle.state_layer_color**

Handle state layer color.
[`state_layer_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.slider.slider.MDSliderHandle.state_layer_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.slider.slider.MDSliderHandle.on_enter**

Fired when mouse enter the bbox of the widget.
Animates the display of the slider handle layer.

**kivymd.uix.slider.slider.MDSliderHandle.on_leave**

Fired when the mouse goes outside the widget border.
Animates the hiding of the slider handle layer.

**kivymd.uix.slider.slider.MDSliderValueLabel**

Implements the value label.
For more information, see in the [`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel)
class documentation.
Added in version 2.0.0.

**kivymd.uix.slider.slider.MDSliderValueLabel.size**

Container size for the label value.
`handle_anim_transition` is an [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [dp(36), dp(36)].

---

## API - [`kivymd.uix.sliverappbar.sliverappbar`](https://kivymd.readthedocs.io/en/latest/components/sliverappbar/)

**kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbarContent**

Implements a box for a scrollable list of custom items.
For more information, see in the
[`MDBoxLayout`](https://kivymd.readthedocs.io/en/boxlayout/#kivymd.uix.boxlayout.MDBoxLayout) class documentation.

**kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbarHeader**

Sliver app bar header class.
For more information, see in the
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout) class documentation.

**kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar**

Sliver appbar class.
For more information, see in the
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
classes documentation.

**kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.background_color**

Background color of appbar in (r, g, b, a) or string format.
[`background_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.background_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.max_height**

Distance from top of screen to start of custom list content.

[`max_height`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.max_height) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to Window.height / 2.

**kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.hide_appbar**

Whether to hide the appbar when scrolling through a list
of custom content.
Changed in version 2.0.0:Rename hide_toolbar to hide_appbar attribute.

[`hide_appbar`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.hide_appbar) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to None.

**kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.radius**

Box radius for custom item list.

[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [20].

**kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.max_opacity**

Maximum background transparency value for the
[`MDSliverAppbarHeader`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbarHeader) class.

[`max_opacity`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.max_opacity) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 1.

**kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.on_hide_appbar**

Fired when the hide_appbar value changes.

**kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.on_scroll_content**

Fired when the list of custom content is being scrolled.

**kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.on_background_color**

Fired when the background_color value changes.

**kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.on_vbar**

**kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.sliverappbar.sliverappbar.MDSliverAppbar.on__appbar**

---

## API - [`kivymd.uix.snackbar.snackbar`](https://kivymd.readthedocs.io/en/latest/components/snackbar/)

**kivymd.uix.snackbar.snackbar.MDSnackbarButtonContainer**

The class implements a container for placing snackbar buttons.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout) classes documentation.

**kivymd.uix.snackbar.snackbar.MDSnackbarButtonContainer.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.snackbar.snackbar.MDSnackbarCloseButton**

Snackbar closed button class.
For more information, see in the
[`MDIconButton`](https://kivymd.readthedocs.io/en/button/#kivymd.uix.button.button.MDIconButton) class documentation.

**kivymd.uix.snackbar.snackbar.MDSnackbarActionButtonText**

The class implements the text for the [`MDSnackbarActionButton`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.snackbar.snackbar.MDSnackbarActionButton)
class.
Changed in version 2.2.0.
For more information, see in the
[`MDButtonText`](https://kivymd.readthedocs.io/en/button/#kivymd.uix.button.button.MDButtonText) class documentation.

**kivymd.uix.snackbar.snackbar.MDSnackbarActionButton**

Snackbar action button class.
For more information, see in the
[`MDButton`](https://kivymd.readthedocs.io/en/button/#kivymd.uix.button.button.MDButton) class documentation.

**kivymd.uix.snackbar.snackbar.MDSnackbar**

Snackbar class.
Changed in version 1.2.0:Rename BaseSnackbar to MDSnackbar class.
For more information, see in the
[`MotionShackBehavior`](https://kivymd.readthedocs.io/behaviors/motion/#kivymd.uix.behaviors.motion_behavior.MotionShackBehavior) and
[`MDCard`](https://kivymd.readthedocs.io/en/card/#kivymd.uix.card.card.MDCard) and
class documentation.

**kivymd.uix.snackbar.snackbar.MDSnackbar.duration**

The amount of time that the snackbar will stay on screen for.
[`duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.snackbar.snackbar.MDSnackbar.duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 3.

**kivymd.uix.snackbar.snackbar.MDSnackbar.auto_dismiss**

Whether to use automatic closing of the snackbar or not.
[`auto_dismiss`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.snackbar.snackbar.MDSnackbar.auto_dismiss) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivymd.uix.snackbar.snackbar.MDSnackbar.radius**

Snackbar radius.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.snackbar.snackbar.MDSnackbar.radius) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [dp(4), dp(4), dp(4), dp(4)]

**kivymd.uix.snackbar.snackbar.MDSnackbar.background_color**

The background color in (r, g, b, a) or string format of the snackbar.
[`background_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.snackbar.snackbar.MDSnackbar.background_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.snackbar.snackbar.MDSnackbar.dismiss**

Dismiss the snackbar.

**kivymd.uix.snackbar.snackbar.MDSnackbar.open**

Show the snackbar.

**kivymd.uix.snackbar.snackbar.MDSnackbar.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.snackbar.snackbar.MDSnackbar.on_open**

Fired when a snackbar opened.

**kivymd.uix.snackbar.snackbar.MDSnackbar.on_dismiss**

Fired when a snackbar closed.

**kivymd.uix.snackbar.snackbar.MDSnackbarText**

The class implements the text.
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) class documentation.

**kivymd.uix.snackbar.snackbar.MDSnackbarSupportingText**

The class implements the supporting text.
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) class documentation.

---

## API - [`kivymd.uix.stacklayout`](https://kivymd.readthedocs.io/en/latest/components/stacklayout/)

**kivymd.uix.stacklayout.MDStackLayout**

Stack layout class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`StackLayout`](https://kivy.org/doc/stable/api-kivy.uix.stacklayout.html#kivy.uix.stacklayout.StackLayout) and
[`MDAdaptiveWidget`](https://kivymd.readthedocs.io/api/kivymd/uix/#kivymd.uix.MDAdaptiveWidget)
classes documentation.

---

## API - [`kivymd.uix.swiper.swiper`](https://kivymd.readthedocs.io/en/latest/components/swiper/)

**kivymd.uix.swiper.swiper.MDSwiperItem**

Swiper item class.
For more information, see in the
[`MDBoxLayout`](https://kivymd.readthedocs.io/en/boxlayout/#kivymd.uix.boxlayout.MDBoxLayout) class documentation.

**kivymd.uix.swiper.swiper.MDSwiper**

Swiper class.
For more information, see in the
[`ScrollView`](https://kivy.org/doc/stable/api-kivy.uix.scrollview.html#kivy.uix.scrollview.ScrollView) class documentation.

**kivymd.uix.swiper.swiper.MDSwiper.items_spacing**

The space between each [`MDSwiperItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiperItem).
[`items_spacing`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiper.items_spacing) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 20dp.

**kivymd.uix.swiper.swiper.MDSwiper.transition_duration**

Duration of switching between [`MDSwiperItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiperItem).
[`transition_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiper.transition_duration) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivymd.uix.swiper.swiper.MDSwiper.size_duration**

Duration of changing the size of [`MDSwiperItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiperItem).
[`transition_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiper.transition_duration) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivymd.uix.swiper.swiper.MDSwiper.size_transition**

The type of animation used for changing the size of [`MDSwiperItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiperItem).
[`size_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiper.size_transition) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to out_quad.

**kivymd.uix.swiper.swiper.MDSwiper.swipe_transition**

The type of animation used for swiping.
[`swipe_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiper.swipe_transition) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to out_quad.

**kivymd.uix.swiper.swiper.MDSwiper.swipe_distance**

Distance to move before swiping the [`MDSwiperItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiperItem).
[`swipe_distance`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiper.swipe_distance) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 70dp.

**kivymd.uix.swiper.swiper.MDSwiper.width_mult**

This number is multiplied by [`items_spacing`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiper.items_spacing) x2 and
then subtracted from the width of window to specify the width of
[`MDSwiperItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiperItem). So by decreasing the [`width_mult`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiper.width_mult) the width
of [`MDSwiperItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiperItem) increases and vice versa.
[`width_mult`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiper.width_mult) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 3.

**kivymd.uix.swiper.swiper.MDSwiper.swipe_on_scroll**

Wheter to swipe on mouse wheel scrolling or not.
[`swipe_on_scroll`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiper.swipe_on_scroll) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivymd.uix.swiper.swiper.MDSwiper.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.swiper.swiper.MDSwiper.remove_widget**

Remove a widget from the children of this widget.

**kivymd.uix.swiper.swiper.MDSwiper.set_current**

Switch to given [`MDSwiperItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiperItem) index.

**kivymd.uix.swiper.swiper.MDSwiper.get_current_index**

Returns the current [`MDSwiperItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiperItem) index.

**kivymd.uix.swiper.swiper.MDSwiper.get_current_item**

Returns the current [`MDSwiperItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiperItem) instance.

**kivymd.uix.swiper.swiper.MDSwiper.get_items**

Returns the list of [`MDSwiperItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiperItem) children.

**kivymd.uix.swiper.swiper.MDSwiper.on_swipe**

**kivymd.uix.swiper.swiper.MDSwiper.on_pre_swipe**

**kivymd.uix.swiper.swiper.MDSwiper.on_overswipe_right**

**kivymd.uix.swiper.swiper.MDSwiper.on_overswipe_left**

**kivymd.uix.swiper.swiper.MDSwiper.on_swipe_left**

**kivymd.uix.swiper.swiper.MDSwiper.on_swipe_right**

**kivymd.uix.swiper.swiper.MDSwiper.swipe_left**

**kivymd.uix.swiper.swiper.MDSwiper.swipe_right**

**kivymd.uix.swiper.swiper.MDSwiper.on_scroll_start**

**kivymd.uix.swiper.swiper.MDSwiper.on_touch_down**

Receive a touch down event.

**kivymd.uix.swiper.swiper.MDSwiper.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.swiper.swiper.MDSwiper.on_touch_down) for more information.

---

## API - [`kivymd.uix.tab.tab`](https://kivymd.readthedocs.io/en/latest/components/tabs/)

**kivymd.uix.tab.tab.MDTabsBadge**

Implements an badge for secondary tabs.
Added in version 2.0.0.
For more information, see in the
[`MDBadge`](https://kivymd.readthedocs.io/en/badge/#kivymd.uix.badge.badge.MDBadge) class documentation.

**kivymd.uix.tab.tab.MDTabsCarousel**

Implements a carousel for user-generated content.
For more information, see in the
[`Carousel`](https://kivy.org/doc/stable/api-kivy.uix.carousel.html#kivy.uix.carousel.Carousel) class documentation.

**kivymd.uix.tab.tab.MDTabsCarousel.lock_swiping**

If True - disable switching tabs by swipe.
[`lock_swiping`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsCarousel.lock_swiping) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.tab.tab.MDTabsCarousel.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See `on_touch_down()` for more information.

**kivymd.uix.tab.tab.MDTabsCarousel.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.tab.tab.MDTabsItemText**

Implements an label for the [`MDTabsItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsItem) class.
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) class documentation.
Added in version 2.0.0.

**kivymd.uix.tab.tab.MDTabsItemIcon**

Implements an icon for the [`MDTabsItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsItem) class.
For more information, see in the
[`MDIcon`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDIcon) class documentation.
Added in version 2.0.0.

**kivymd.uix.tab.tab.MDTabsItem**

Implements a item with an icon and text for [`MDTabsPrimary`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsPrimary) class.
Added in version 2.0.0.
For more information, see in the
`MDTabsItemBase` and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
classes documentation.

**kivymd.uix.tab.tab.MDTabsItem.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.tab.tab.MDTabsPrimary**

Tabs primary class.
Changed in version 2.0.0:Rename from MDTabs to MDTabsPrimary class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
classes documentation.

**kivymd.uix.tab.tab.MDTabsPrimary.md_bg_color**

The background color of the widget.
[`md_bg_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsPrimary.md_bg_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.tab.tab.MDTabsPrimary.label_only**

Tabs with a label only or with an icon and a label.
Added in version 2.0.0.
[`label_only`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsPrimary.label_only) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.tab.tab.MDTabsPrimary.allow_stretch**

Whether to stretch tabs to the width of the panel.
[`allow_stretch`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsPrimary.allow_stretch) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivymd.uix.tab.tab.MDTabsPrimary.lock_swiping**

If True - disable switching tabs by swipe.
[`lock_swiping`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsPrimary.lock_swiping) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.tab.tab.MDTabsPrimary.anim_duration**

Duration of the slide animation.
[`anim_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsPrimary.anim_duration) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivymd.uix.tab.tab.MDTabsPrimary.indicator_anim**

Tab indicator animation. If you want use animation set it to `True`.
Changed in version 2.0.0:Rename from tab_indicator_anim to indicator_anim attribute.
[`indicator_anim`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsPrimary.indicator_anim) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivymd.uix.tab.tab.MDTabsPrimary.indicator_radius**

Radius of the tab indicator.
Added in version 2.0.0.
[`indicator_radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsPrimary.indicator_radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [dp(2), dp(2), 0, 0].

**kivymd.uix.tab.tab.MDTabsPrimary.indicator_height**

Height of the tab indicator.
Changed in version 2.0.0:Rename from tab_indicator_height to indicator_height attribute.
[`indicator_height`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsPrimary.indicator_height) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to ‘4dp’.

**kivymd.uix.tab.tab.MDTabsPrimary.indicator_duration**

The duration of the animation of the indicator movement when switching
tabs.
Added in version 2.0.0.
[`indicator_duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsPrimary.indicator_duration) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.5.

**kivymd.uix.tab.tab.MDTabsPrimary.indicator_transition**

The transition name of animation of the indicator movement when switching
tabs.
Added in version 2.0.0.
[`indicator_transition`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsPrimary.indicator_transition) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to [`](https://kivymd.readthedocs.io/en/latest/#id2)’out_expo’.

**kivymd.uix.tab.tab.MDTabsPrimary.last_scroll_x**

Is the carousel reference of the next tab/slide.
When you go from ‘Tab A’ to ‘Tab B’, ‘Tab B’ will be the
target tab/slide of the carousel.
[`last_scroll_x`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsPrimary.last_scroll_x) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivymd.uix.tab.tab.MDTabsPrimary.target**

It is the carousel reference of the next tab / slide.
When you go from ‘Tab A’ to ‘Tab B’, ‘Tab B’ will be the
target tab / slide of the carousel.
[`target`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsPrimary.target) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and default to None.

**kivymd.uix.tab.tab.MDTabsPrimary.indicator**

It is the `SmoothRoundedRectangle`
instruction reference of the tab indicator.
[`indicator`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsPrimary.indicator) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivymd.uix.tab.tab.MDTabsPrimary.get_last_scroll_x**

**kivymd.uix.tab.tab.MDTabsPrimary.get_rect_instruction**

**kivymd.uix.tab.tab.MDTabsPrimary.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.tab.tab.MDTabsPrimary.do_autoscroll_tabs**

Automatically scrolls the list of tabs when swiping the carousel
slide (related content).
Changed in version 2.0.0:Rename from tab_bar_autoscroll to do_autoscroll_tabs method.

**kivymd.uix.tab.tab.MDTabsPrimary.android_animation**

Fired when swiping a carousel slide (related content).

**kivymd.uix.tab.tab.MDTabsPrimary.update_indicator**

Update position and size of the indicator.

**kivymd.uix.tab.tab.MDTabsPrimary.switch_tab**

Switches tabs by tab object/tab text/tab icon name.

**kivymd.uix.tab.tab.MDTabsPrimary.set_active_item**

Sets the active tab item.

**kivymd.uix.tab.tab.MDTabsPrimary.get_tabs_list**

Returns a list of [`MDTabsItem`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsItem) objects.
Changed in version 2.0.0:Rename from get_tab_list to get_tabs_list method.

**kivymd.uix.tab.tab.MDTabsPrimary.get_slides_list**

Returns a list of user tab objects.
Changed in version 2.0.0:Rename from get_slides to get_slides_list method.

**kivymd.uix.tab.tab.MDTabsPrimary.get_current_tab**

Returns current tab object.
Added in version 1.0.0.

**kivymd.uix.tab.tab.MDTabsPrimary.get_current_related_content**

Returns the carousel slide object (related content).
Added in version 2.0.0.

**kivymd.uix.tab.tab.MDTabsPrimary.on_tab_switch**

This event is launched every time the current tab is changed.

**kivymd.uix.tab.tab.MDTabsPrimary.on_slide_progress**

This event is deployed every available frame while the tab is
scrolling.

**kivymd.uix.tab.tab.MDTabsPrimary.on_carousel_index**

Fired when the Tab index have changed.
This event is deployed by the builtin carousel of the class.

**kivymd.uix.tab.tab.MDTabsPrimary.on_size**

Fired when the application screen size changes.

**kivymd.uix.tab.tab.MDTabsPrimary.recalculate_tab_widths**

Recalculates and updates the width of each tab in the tab bar.
This method ensures that all tabs are evenly distributed across the
available horizontal space when allow_stretch is enabled. It is
automatically called after a new tab is added.
If no tabs are present, the method exits without making changes.

**kivymd.uix.tab.tab.MDTabsItemSecondary**

Implements a item with an icon and text for [`MDTabsSecondary`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsSecondary)
class.
Added in version 2.0.0.
For more information, see in the
`MDTabsItemBase` and
[`AnchorLayout`](https://kivy.org/doc/stable/api-kivy.uix.anchorlayout.html#kivy.uix.anchorlayout.AnchorLayout)
classes documentation.

**kivymd.uix.tab.tab.MDTabsItemSecondary.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.tab.tab.MDTabsSecondary**

Tabs secondary class.
Added in version 2.0.0.
For more information, see in the
[`MDTabsPrimary`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsPrimary) class documentation.

**kivymd.uix.tab.tab.MDTabsSecondary.indicator_radius**

Radius of the tab indicator.
[`indicator_radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsSecondary.indicator_radius) is an [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty)
and defaults to [0, 0, 0, 0].

**kivymd.uix.tab.tab.MDTabsSecondary.indicator_height**

Height of the tab indicator.
[`indicator_height`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tab.tab.MDTabsSecondary.indicator_height) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to ‘2dp’.

---

## API - [`kivymd.uix.textfield.textfield`](https://kivymd.readthedocs.io/en/latest/components/text-fields/)

**kivymd.uix.textfield.textfield.AutoFormatTelephoneNumber**

Implements automatic formatting of the text entered in the text field
according to the mask, for example ‘+38 (###) ### ## ##’.

**kivymd.uix.textfield.textfield.AutoFormatTelephoneNumber.isnumeric**

**kivymd.uix.textfield.textfield.AutoFormatTelephoneNumber.do_backspace**

Do backspace operation from the current cursor position.

**kivymd.uix.textfield.textfield.AutoFormatTelephoneNumber.field_filter**

**kivymd.uix.textfield.textfield.AutoFormatTelephoneNumber.format**

**kivymd.uix.textfield.textfield.Validator**

Container class for various validation methods.

**kivymd.uix.textfield.textfield.Validator.datetime_date**

The last valid date as a <class ‘datetime.date’> object.
[`datetime_date`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.Validator.datetime_date) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivymd.uix.textfield.textfield.Validator.date_interval**

The date interval that is valid for input.
Can be entered as <class ‘datetime.date’> objects or a string format.
Both values or just one value can be entered.
In string format, must follow the current date_format.
Example: Given date_format -> “mm/dd/yyyy”
Input examples -> “12/31/1900”, “12/31/2100” or “12/31/1900”, None.
[`date_interval`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.Validator.date_interval) is an [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [None, None].

**kivymd.uix.textfield.textfield.Validator.date_format**

Format of date strings that will be entered.
Available options are: ‘dd/mm/yyyy’, ‘mm/dd/yyyy’, ‘yyyy/mm/dd’.
[`date_format`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.Validator.date_format) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to None.

**kivymd.uix.textfield.textfield.Validator.is_number_valid**

Checks if the text contains only digits.

**kivymd.uix.textfield.textfield.Validator.is_email_valid**

Checks the validity of the email.

**kivymd.uix.textfield.textfield.Validator.is_time_valid**

Checks the validity of the time.

**kivymd.uix.textfield.textfield.Validator.is_date_valid**

Checks the validity of the date.

**kivymd.uix.textfield.textfield.Validator.on_date_interval**

Default event handler for date_interval input.

**kivymd.uix.textfield.textfield.BaseTextFieldLabel**

Base texture for [`MDTextField`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField) class (helper text, max length,
hint text).
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) class documentation.
Added in version 2.0.0.

**kivymd.uix.textfield.textfield.BaseTextFieldLabel.text_color_normal**

Text color in (r, g, b, a) or string format when text field is out
of focus.
Added in version 1.0.0.
Changed in version 2.0.0:The property was moved from class:~MDTextField class and renamed
from helper_text_color_normal to text_color_normal.
Declarative KV styleDeclarative Python style

[`text_color_normal`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.BaseTextFieldLabel.text_color_normal) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.textfield.textfield.BaseTextFieldLabel.text_color_focus**

Text color in (r, g, b, a) or string format when the text field has
focus.
Added in version 1.0.0.
Changed in version 2.0.0:The property was moved from class:~MDTextField class and renamed
from helper_text_color_focus to text_color_focus.
Declarative KV styleDeclarative Python style

[`text_color_focus`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.BaseTextFieldLabel.text_color_focus) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.textfield.textfield.MDTextFieldHelperText**

Implements the helper text label.
For more information, see in the [`BaseTextFieldLabel`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.BaseTextFieldLabel)
class documentation.
Added in version 2.0.0.

**kivymd.uix.textfield.textfield.MDTextFieldHelperText.mode**

Helper text mode. Available options are: ‘on_error’, ‘persistent’,
‘on_focus’.
Changed in version 2.0.0:The property was moved from class:~MDTextField class and renamed
from helper_text_mode to mode.
On focus[#](https://kivymd.readthedocs.io/en/latest/#on-focus)
Declarative KV styleDeclarative Python style
On error[#](https://kivymd.readthedocs.io/en/latest/#on-error)
Declarative KV styleDeclarative Python style
Persistent[#](https://kivymd.readthedocs.io/en/latest/#persistent)
Declarative KV styleDeclarative Python style

[`mode`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextFieldHelperText.mode) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘on_focus’.

**kivymd.uix.textfield.textfield.MDTextFieldMaxLengthText**

Implements the max length text label.
For more information, see in the [`BaseTextFieldLabel`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.BaseTextFieldLabel)
class documentation.
Added in version 2.0.0.

**kivymd.uix.textfield.textfield.MDTextFieldMaxLengthText.max_text_length**

Maximum allowed value of characters in a text field.
Changed in version 2.0.0:The property was moved from class:~MDTextField.
Declarative KV styleDeclarative Python style

[`max_text_length`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextFieldMaxLengthText.max_text_length) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to None.

**kivymd.uix.textfield.textfield.MDTextFieldHintText**

Implements the hint text label.
For more information, see in the [`BaseTextFieldLabel`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.BaseTextFieldLabel)
class documentation.
Added in version 2.0.0.
Declarative KV styleDeclarative Python style

**kivymd.uix.textfield.textfield.BaseTextFieldIcon**

Base texture for [`MDTextField`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField) class (helper text, max length,
hint text).
For more information, see in the [`MDIcon`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDIcon)
class documentation.
Changed in version 2.0.0.

**kivymd.uix.textfield.textfield.BaseTextFieldIcon.icon_color_normal**

Icon color in (r, g, b, a) or string format when text field is out
of focus.
Added in version 1.0.0.
Changed in version 2.0.0:The property was moved from class:~MDTextField class and renamed
from icon_right_color_normal/icon_left_color_normal
to icon_color_normal.
Declarative KV styleDeclarative Python style

[`icon_color_normal`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.BaseTextFieldIcon.icon_color_normal) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.textfield.textfield.BaseTextFieldIcon.icon_color_focus**

Icon color in (r, g, b, a) or string format when the text field has
focus.
Added in version 1.0.0.
Changed in version 2.0.0:The property was moved from class:~MDTextField class and renamed
from icon_right_color_focus/icon_left_color_focus `
to `icon_color_focus.
Declarative KV styleDeclarative Python style

[`icon_color_focus`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.BaseTextFieldIcon.icon_color_focus) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.textfield.textfield.BaseTextFieldIcon.on_icon_color_normal**

Called when the icon_color_normal property of the icon is changed.
If the associated text field is set, this method triggers an update
to the icon’s color appearance, ensuring that the correct color is
used based on the focus state of the text field.
Typically used to visually reflect property changes in real time
in response to user interaction or theme updates.

**kivymd.uix.textfield.textfield.MDTextFieldLeadingIcon**

Implements the leading icon.
For more information, see in the [`BaseTextFieldIcon`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.BaseTextFieldIcon)
class documentation.
Added in version 2.0.0.
Declarative KV styleDeclarative Python style

**kivymd.uix.textfield.textfield.MDTextFieldTrailingIcon**

Implements the trailing icon.
For more information, see in the [`BaseTextFieldIcon`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.BaseTextFieldIcon)
class documentation.
Added in version 2.0.0.
Declarative KV styleDeclarative Python style

**kivymd.uix.textfield.textfield.MDTextField**

Textfield class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`TextInput`](https://kivy.org/doc/stable/api-kivy.uix.textinput.html#kivy.uix.textinput.TextInput) and
[`Validator`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.Validator) and
[`AutoFormatTelephoneNumber`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.AutoFormatTelephoneNumber) and
[`StateLayerBehavior`](https://kivymd.readthedocs.io/behaviors/state-layer/#kivymd.uix.behaviors.state_layer_behavior.StateLayerBehavior)
classes documentation.

**kivymd.uix.textfield.textfield.MDTextField.font_style**

Name of the style for the input text.
Added in version 2.0.0.

[`font_style`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.font_style) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘Body’.

**kivymd.uix.textfield.textfield.MDTextField.role**

Role of font style.
Added in version 2.0.0.

[`role`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.role) is an [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘large’.

**kivymd.uix.textfield.textfield.MDTextField.mode**

Text field mode. Available options are: ‘outlined’, ‘filled’.
[`mode`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.mode) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘outlined’.

**kivymd.uix.textfield.textfield.MDTextField.error_color**

Error color in (r, g, b, a) or string format for required = True
or when the text field is in error state.
[`error_color`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.error_color) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.textfield.textfield.MDTextField.error**

If True, then the text field goes into error mode.
[`error`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.error) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.textfield.textfield.MDTextField.text_color_normal**

Text color in (r, g, b, a) or string format when text field is out of focus.
Added in version 1.0.0.
Declarative KV styleDeclarative Python style

[`text_color_normal`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.text_color_normal) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.textfield.textfield.MDTextField.text_color_focus**

Text color in (r, g, b, a) or string format when text field has focus.
Added in version 1.0.0.
Declarative KV styleDeclarative Python style

[`text_color_focus`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.text_color_focus) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.textfield.textfield.MDTextField.radius**

The corner radius for a text field in filled/outlined mode.
[`radius`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.radius) is a [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty) and
defaults to [dp(4), dp(4), 0, 0].

**kivymd.uix.textfield.textfield.MDTextField.required**

Required text. If True then the text field requires text.
[`required`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.required) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivymd.uix.textfield.textfield.MDTextField.line_color_normal**

Line color normal (active indicator) in (r, g, b, a) or string format.
Declarative KV styleDeclarative Python style

[`line_color_normal`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.line_color_normal) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.textfield.textfield.MDTextField.line_color_focus**

Line color focus (active indicator) in (r, g, b, a) or string format.
Declarative KV styleDeclarative Python style

[`line_color_focus`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.line_color_focus) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.textfield.textfield.MDTextField.fill_color_normal**

Fill background color in (r, g, b, a) or string format in ‘fill’ mode when]
text field is out of focus.
Declarative KV styleDeclarative Python style

[`fill_color_normal`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.fill_color_normal) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.textfield.textfield.MDTextField.fill_color_focus**

Fill background color in (r, g, b, a) or string format in ‘fill’ mode when
the text field has focus.
Declarative KV styleDeclarative Python style

[`fill_color_focus`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.fill_color_focus) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to None.

**kivymd.uix.textfield.textfield.MDTextField.max_height**

Maximum height of the text box when multiline = True.
Declarative KV styleDeclarative Python style

[`max_height`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.max_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivymd.uix.textfield.textfield.MDTextField.phone_mask**

This property has not yet been implemented and it is not recommended to
use it yet.
[`phone_mask`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.phone_mask) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘’.

**kivymd.uix.textfield.textfield.MDTextField.validator**

The type of text field for entering Email, time, etc.
Automatically sets the type of the text field as “error” if the user input
does not match any of the set validation types.
Available options are: ‘date’, ‘email’, ‘time’, ‘phone’, number.
When using ‘date’, `date_format` must be defined.
Added in version 1.1.0.
Declarative KV styleDeclarative Python style

Declarative KV styleDeclarative Python style

[`validator`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.textfield.textfield.MDTextField.validator) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to None.

**kivymd.uix.textfield.textfield.MDTextField.update_colors**

Fired when the primary_palette or theme_style value changes.

**kivymd.uix.textfield.textfield.MDTextField.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.textfield.textfield.MDTextField.set_texture_color**

Animates the color of the
leading/trailing icons/hint/helper/max length text.

**kivymd.uix.textfield.textfield.MDTextField.get_adjusted_pos_max_length_label**

Calculates the position of the max length label.

**kivymd.uix.textfield.textfield.MDTextField.get_adjusted_pos_helper_text_label**

Calculates the position of the helper text label based on the
textfield mode.

**kivymd.uix.textfield.textfield.MDTextField.get_adjusted_pos_trailing_icon**

Calculates the adjusted position of the trailing icon.

**kivymd.uix.textfield.textfield.MDTextField.get_adjusted_pos_leading_icon**

Calculates the adjusted position of the leading icon based on the
textfield mode and icon size.

**kivymd.uix.textfield.textfield.MDTextField.get_adjusted_pos_hint_text_label**

Calculates the adjusted position of the hint text label based on the
presence of a leading icon and whether the textfield is multiline.

**kivymd.uix.textfield.textfield.MDTextField.set_pos_hint_text**

Animates the x-axis width and y-axis height of the hint text.

**kivymd.uix.textfield.textfield.MDTextField.set_hint_text_font_size**

Animates the font size of the hint text.

**kivymd.uix.textfield.textfield.MDTextField.set_space_in_line**

Animates the length of the right line of the text field for the
hint text.

**kivymd.uix.textfield.textfield.MDTextField.set_max_text_length**

Fired when text is entered into a text field.
Set max length text and updated max length texture.

**kivymd.uix.textfield.textfield.MDTextField.adjust_height**

Adjusts the height of the text field in multiline mode.

**kivymd.uix.textfield.textfield.MDTextField.set_text**

Fired when text is entered into a text field.

**kivymd.uix.textfield.textfield.MDTextField.on_focus**

Fired when the focus value changes.

**kivymd.uix.textfield.textfield.MDTextField.on_disabled**

Fired when the disabled value changes.

**kivymd.uix.textfield.textfield.MDTextField.on_error**

Changes the primary colors of the text box to match the error value
(text field is in an error state or not).

**kivymd.uix.textfield.textfield.MDTextField.on_height**

---

## API - [`kivymd.uix.tooltip.tooltip`](https://kivymd.readthedocs.io/en/latest/components/tooltip/)

**kivymd.uix.tooltip.tooltip.MDTooltip**

Tooltip class.
For more information, see in the
[`TouchBehavior`](https://kivymd.readthedocs.io/behaviors/touch/#kivymd.uix.behaviors.touch_behavior.TouchBehavior)
class documentation.

**kivymd.uix.tooltip.tooltip.MDTooltip.tooltip_display_delay**

Tooltip display delay.

[`tooltip_display_delay`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tooltip.tooltip.MDTooltip.tooltip_display_delay) is an [`BoundedNumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BoundedNumericProperty)
and defaults to 0, min of 0 & max of 4.

**kivymd.uix.tooltip.tooltip.MDTooltip.shift_y**

Y-offset of tooltip to the top.
[`shift_y`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tooltip.tooltip.MDTooltip.shift_y) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivymd.uix.tooltip.tooltip.MDTooltip.shift_right**

Shifting the tooltip to the right.
Added in version 1.0.0.
[`shift_right`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tooltip.tooltip.MDTooltip.shift_right) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivymd.uix.tooltip.tooltip.MDTooltip.shift_left**

Shifting the tooltip to the left.
Added in version 1.0.0.
[`shift_left`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tooltip.tooltip.MDTooltip.shift_left) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivymd.uix.tooltip.tooltip.MDTooltip.delete_clock**

Removes a key event from touch.ud.

**kivymd.uix.tooltip.tooltip.MDTooltip.adjust_tooltip_position**

Returns the coordinates of the tooltip that fit into the borders
of the screen.

**kivymd.uix.tooltip.tooltip.MDTooltip.display_tooltip**

Adds a tooltip widget to the screen and animates its display.

**kivymd.uix.tooltip.tooltip.MDTooltip.animation_tooltip_show**

Animation of opening tooltip on the screen.

**kivymd.uix.tooltip.tooltip.MDTooltip.animation_tooltip_dismiss**

Animation of closing tooltip on the screen.
Added in version 1.0.0.

**kivymd.uix.tooltip.tooltip.MDTooltip.remove_tooltip**

Removes the tooltip widget from the screen.

**kivymd.uix.tooltip.tooltip.MDTooltip.add_widget**

Add a new widget as a child of this widget.

**kivymd.uix.tooltip.tooltip.MDTooltip.on_long_touch**

Fired when the widget is pressed for a long time.

**kivymd.uix.tooltip.tooltip.MDTooltip.on_enter**

Fired when mouse enter the bbox of the widget.

**kivymd.uix.tooltip.tooltip.MDTooltip.on_leave**

Fired when the mouse goes outside the widget border.

**kivymd.uix.tooltip.tooltip.MDTooltip.on_open**

Default display event handler.
Changed in version 2.0.0:Rename from on_show to on_open.

**kivymd.uix.tooltip.tooltip.MDTooltip.on_dismiss**

Default dismiss event handler.
Added in version 1.0.0.

**kivymd.uix.tooltip.tooltip.MDTooltipPlain**

Tooltip plain class.
Added in version 2.0.0.
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) and
[`ScaleBehavior`](https://kivymd.readthedocs.io/behaviors/scale/#kivymd.uix.behaviors.scale_behavior.ScaleBehavior)
classes documentation.

**kivymd.uix.tooltip.tooltip.MDTooltipRichSupportingText**

Implements supporting text for the [`MDTooltipRich`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tooltip.tooltip.MDTooltipRich) class.
Added in version 2.0.0.
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) class documentation.

**kivymd.uix.tooltip.tooltip.MDTooltipRichSubhead**

Implements subhead text for the [`MDTooltipRich`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tooltip.tooltip.MDTooltipRich) class.
Added in version 2.0.0.
For more information, see in the
[`MDLabel`](https://kivymd.readthedocs.io/en/label/#kivymd.uix.label.label.MDLabel) class documentation.

**kivymd.uix.tooltip.tooltip.MDTooltipRichActionButton**

Implements action button for the [`MDTooltipRich`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tooltip.tooltip.MDTooltipRich) class.
Added in version 2.0.0.
For more information, see in the
[`MDButton`](https://kivymd.readthedocs.io/en/button/#kivymd.uix.button.button.MDButton) class documentation.

**kivymd.uix.tooltip.tooltip.MDTooltipRichActionButton.on_enter**

Fired when mouse enter the bbox of the widget.

**kivymd.uix.tooltip.tooltip.MDTooltipRichActionButton.on_leave**

Fired when the mouse goes outside the widget border.

**kivymd.uix.tooltip.tooltip.MDTooltipRich**

Tooltip rich class.
Added in version 2.0.0.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`CommonElevationBehavior`](https://kivymd.readthedocs.io/behaviors/elevation/#kivymd.uix.behaviors.elevation.CommonElevationBehavior) and
[`ScaleBehavior`](https://kivymd.readthedocs.io/behaviors/scale/#kivymd.uix.behaviors.scale_behavior.ScaleBehavior) and
[`StateLayerBehavior`](https://kivymd.readthedocs.io/behaviors/state-layer/#kivymd.uix.behaviors.state_layer_behavior.StateLayerBehavior) and
[`BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout) and
classes documentation.

**kivymd.uix.tooltip.tooltip.MDTooltipRich.auto_dismiss**

This property determines if the view is automatically dismissed when
the cursor goes outside of the tooltip body.
[`auto_dismiss`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.tooltip.tooltip.MDTooltipRich.auto_dismiss) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivymd.uix.tooltip.tooltip.MDTooltipRich.on_leave**

Fired when the mouse goes outside the widget border.

**kivymd.uix.tooltip.tooltip.MDTooltipRich.dismiss**

Hides the tooltip.

---

## API - [`kivymd.uix.transition.transition`](https://kivymd.readthedocs.io/en/latest/components/transition/)

**kivymd.uix.transition.transition.MDTransitionBase**

TransitionBase is used to animate 2 screens within the
[`MDScreenManager`](https://kivymd.readthedocs.io/en/screenmanager/#kivymd.uix.screenmanager.MDScreenManager).
For more
information, see in the [`TransitionBase`](https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html#kivy.uix.screenmanager.TransitionBase)
class documentation.

**kivymd.uix.transition.transition.MDTransitionBase.start**

(internal) Starts the transition. This is automatically
called by the `ScreenManager`.

**kivymd.uix.transition.transition.MDTransitionBase.animated_hero_in**

Animates the flight of heroes from screen **A** to screen **B**.

**kivymd.uix.transition.transition.MDTransitionBase.animated_hero_out**

Animates the flight of heroes from screen **B** to screen **A**.

**kivymd.uix.transition.transition.MDTransitionBase.on_complete**

Override method.
See :attr:[`](https://kivymd.readthedocs.io/en/latest/#id1)kivy.uix.screenmanager.TransitionBase.on_complete’.

**kivymd.uix.transition.transition.MDSwapTransition**

Swap transition that looks like iOS transition when a new window
appears on the screen.

**kivymd.uix.transition.transition.MDSlideTransition**

Slide Transition, can be used to show a new screen from any direction:
left, right, up or down.

**kivymd.uix.transition.transition.MDFadeSlideTransition**

Slide Transition, can be used to show a new screen from any direction:
left, right, up or down.

**kivymd.uix.transition.transition.MDFadeSlideTransition.start**

(internal) Starts the transition. This is automatically
called by the `ScreenManager`.

**kivymd.uix.transition.transition.MDFadeSlideTransition.on_progress**

**kivymd.uix.transition.transition.MDSharedAxisTransition**

Android default screen transition.
Added in version 2.0.0.

**kivymd.uix.transition.transition.MDSharedAxisTransition.transition_axis**

Axis of the transition. Available values “x”, “y”, and “z”.

[`transition_axis`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.transition.transition.MDSharedAxisTransition.transition_axis) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to “x”.

**kivymd.uix.transition.transition.MDSharedAxisTransition.duration**

Duration in seconds of the transition. Android recommends these intervals:
Android transition values (in seconds)[#](https://kivymd.readthedocs.io/en/latest/#id5)
Name
value
small_1
0.075
small_2
0.15
medium_1
0.2
medium_2
0.25
large_1
0.3
large_2
0.35
[`duration`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.transition.transition.MDSharedAxisTransition.duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.2 (= 200ms).

**kivymd.uix.transition.transition.MDSharedAxisTransition.switch_animation**

Custom material design animation transition.
[`switch_animation`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.transition.transition.MDSharedAxisTransition.switch_animation) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to “easing_emphasized”.

**kivymd.uix.transition.transition.MDSharedAxisTransition.slide_distance**

Distance to which it slides left, right, bottom or up depending on axis.
[`slide_distance`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.transition.transition.MDSharedAxisTransition.slide_distance) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to dp(15).

**kivymd.uix.transition.transition.MDSharedAxisTransition.opposite**

Decides Transition direction.
[`opposite`](https://kivymd.readthedocs.io/en/latest/#kivymd.uix.transition.transition.MDSharedAxisTransition.opposite) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivymd.uix.transition.transition.MDSharedAxisTransition.start**

(internal) Starts the transition. This is automatically
called by the `ScreenManager`.

**kivymd.uix.transition.transition.MDSharedAxisTransition.on_progress**

**kivymd.uix.transition.transition.MDSharedAxisTransition.on_complete**

Override method.
See :attr:[`](https://kivymd.readthedocs.io/en/latest/#id3)kivy.uix.screenmanager.TransitionBase.on_complete’.

---

## API - [`kivymd.uix.widget`](https://kivymd.readthedocs.io/en/latest/components/widget/)

**kivymd.uix.widget.MDWidget**

Widget class.
For more information, see in the
[`DeclarativeBehavior`](https://kivymd.readthedocs.io/behaviors/declarative/#kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior) and
[`ThemableBehavior`](https://kivymd.readthedocs.io/themes/theming/#kivymd.theming.ThemableBehavior) and
[`BackgroundColorBehavior`](https://kivymd.readthedocs.io/behaviors/background-color/#kivymd.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior) and
[`MDAdaptiveWidget`](https://kivymd.readthedocs.io/api/kivymd/uix/#kivymd.uix.MDAdaptiveWidget) and
[`Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget) and
classes documentation.
Added in version 1.0.0.

---

## API - [`kivymd.utils`](https://kivymd.readthedocs.io/en/latest/api/kivymd/utils/)

**kivymd.utils.next_frame**

---

## API - [`kivymd.utils.cubic_bezier`](https://kivymd.readthedocs.io/en/latest/api/kivymd/utils/cubic_bezier/)

**kivymd.utils.cubic_bezier.float_epsilon**

**kivymd.utils.cubic_bezier.cbrt**

**kivymd.utils.cubic_bezier.CubicBezier**

Ported from Android source code.
Represents a cubic Bézier curve interpolator.
A cubic Bézier curve is defined by four control points:
P0 — start point
P1 — first control point
P2 — second control point
P3 — end point
The curve is commonly used in UI animations to define easing behavior.
Given an input progress value x in the range [0, 1], the class calculates
the corresponding output value y on the curve.
This implementation solves the cubic equation required to find the curve
parameter t for a given X value and then evaluates the curve at that
parameter to obtain the interpolated Y value.

**kivymd.utils.cubic_bezier.CubicBezier.p0**

**kivymd.utils.cubic_bezier.CubicBezier.p1**

**kivymd.utils.cubic_bezier.CubicBezier.p2**

**kivymd.utils.cubic_bezier.CubicBezier.p3**

**kivymd.utils.cubic_bezier.CubicBezier.evaluate_cubic**

Evaluates a cubic Bézier polynomial.

**kivymd.utils.cubic_bezier.CubicBezier.clamp_range**

Clamps a calculated root value into the valid Bézier range.
Small floating-point calculation errors are corrected using an
epsilon tolerance. Values outside the acceptable range are converted
to NaN.

**kivymd.utils.cubic_bezier.CubicBezier.close_to**

Checks whether two floating-point numbers are approximately equal.

**kivymd.utils.cubic_bezier.CubicBezier.find_first_cubic_root**

Finds the first valid root of a cubic equation.
The method solves the cubic polynomial generated from the Bézier curve
equation and returns a parameter t within the valid interval [0, 1].

**kivymd.utils.cubic_bezier.CubicBezier.t**

Calculates the interpolated Bézier value for an input progress value.
This method converts an X-axis position into the corresponding Y-axis
position on the cubic Bézier curve.

---

## API - [`kivymd.utils.fpsmonitor`](https://kivymd.readthedocs.io/en/latest/api/kivymd/utils/fpsmonitor/)

**kivymd.utils.fpsmonitor.FpsMonitor**

Fps monitor class.
For more information, see in the
[`Label`](https://kivy.org/doc/stable/api-kivy.uix.label.html#kivy.uix.label.Label) class documentation.

**kivymd.utils.fpsmonitor.FpsMonitor.updated_interval**

FPS refresh rate.
[`updated_interval`](https://kivymd.readthedocs.io/en/latest/#kivymd.utils.fpsmonitor.FpsMonitor.updated_interval) is an [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.5.

**kivymd.utils.fpsmonitor.FpsMonitor.anchor**

Monitor position.
Available option are: ‘top’, ‘bottom’.
[`anchor`](https://kivymd.readthedocs.io/en/latest/#kivymd.utils.fpsmonitor.FpsMonitor.anchor) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘top’.

**kivymd.utils.fpsmonitor.FpsMonitor.start**

Monitor starting.

**kivymd.utils.fpsmonitor.FpsMonitor.update_fps**

---

## API - [`kivymd.utils.set_bars_colors`](https://kivymd.readthedocs.io/en/latest/api/kivymd/utils/set_bars_colors/)

**kivymd.utils.set_bars_colors.set_bars_colors**

Sets the color of the status of the StatusBar and NavigationBar.

Dark icon mode

Added in version 1.0.0.

---

