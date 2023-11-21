import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "PAGETools",
  description: "Documentation for the PAGETools python library",
  base: '/PAGETools/',
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Installation', link: '/installation' },
      { text: 'Tools', link: '/tools/index' },
    ],

    sidebar: [
      {
        text: 'Installation', link: '/installation',
      },
      {
        text: 'Tools',
        items: [
          {
            text: "Analytics",
            items: [
              {
               text: "Get Codec", link: "/tools/analytics/get_codec"
              },
              {
               text: "Get Text Count", link: "/tools/analytics/get_text_count"
              }
            ]
          },
          {
            text: "Management",
            items: [
            ]
          },
          {
            text: "Transformation",
            items: [
              {
               text: "Change Index", link: "/tools/transformation/change_index"
              },
              {
               text: "Extraction", link: "/tools/transformation/extraction"
              },
              {
               text: "Line2Page", link: "/tools/transformation/line2page"
              },
              {
               text: "Regularization", link: "/tools/transformation/regularization"
              },
            ]
          }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/uniwue-zpd/PAGETools' },
      { icon: 'twitter', link: 'https://twitter.com/uniwue_zpd' }
    ]
  }
})
